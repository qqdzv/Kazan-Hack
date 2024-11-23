<template>
    <div class="aiChatPage">
        <header class="chatHeader">
            <CustomIcon id="arrow_left" :width="24" :height="24" @click="goBack" class="icon" />
            <div class="headerText">
                <h4>{{ firstName + ' ' + lastName }}</h4>
                <p>{{ speciality }}</p>
            </div>
        </header>

        <div class="videoButtonWrapper">
            <div @click="fetchDateCall()" :style="{ display: 'flex', backgroundColor: '#D1F3ED', justifyContent: 'center', borderRadius: '12px', padding: '10px', color: '#16C4A4', fontFamily: 'var(--font-main)', width: '220px', fontWeight: 'bold' }">
                <img src="/img/videoCall/startContent.png" />
                <p :style="{ paddingLeft: '5px' }">Записаться</p>
            </div>
        </div>

        <main class="chatBody">
            <div v-for="(message, index) in messages" :key="index" :class="['message', { 'message-user': message.sender_type === 'user', 'message-doctor': message.sender_type === 'doctor' }]">
                <div class="messageBox">
                    <img v-if="message.image_base64" :src="message.image_base64" alt="Отправленное изображение" class="messageImage" />
                    <p v-if="message.text">{{ message.text }}</p>
                </div>

                <span :class="['time', { 'time-user': message.sender_type === 'user', 'time-doctor': message.sender_type === 'doctor' }]">
                    {{ message.created_at ? formatDate(message.created_at).time : '' }}
                </span>

                <MainButton v-if="message.conference_time" text="Видео встреча" :style="{ backgroundColor: '#D1F3ED', text: '#16C4A4' }" class="btn_1" @click="router.push('/videoCall')" :width="220" />
            </div>
        </main>

        <div class="inputBar">
            <CustomIcon id="file" :width="32" :height="32" class="fileIcon" @click="triggerFileInput"></CustomIcon>
            <div class="borderPic"><img v-if="loaded" src="/img/homepage/completePic.png" :width="25" /></div>
            <textarea type="text" placeholder="Сообщение" @keyup.enter="sendMessage" @input="autoResize" v-model="newMessage"></textarea>
            <CustomIcon id="send" :width="32" :height="32" class="sendIcon" @click="sendMessage" />
        </div>

        <input type="file" accept="image/*" ref="fileInput" class="hidden" :style="{ opacity: '0' }" @change="onFileChange" />
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/axios/api';
import CustomIcon from '@/ui/CustomIcon.vue';
import { formatDate } from '@/utils/fortmatDate';
import { useRoleStore } from '@/store/useRoleStore';
import { Doctor, Patient, useUserStore } from '@/store/useUserStore';
import { Message } from './AllChatsPage.vue';
import LoaderComp from '@/components/LoaderComp.vue';
import MainButton from '@/ui/MainButton.vue';

const goToVideoCall = () => {
    console.log('Переход на /videoCall');
    router.push('/videoCall').catch((err) => {
        console.error('Ошибка при переходе:', err);
    });
    window.history.back();
};

interface ChatMessage {
    sender_type: string;
    text?: string;
    created_at?: string;
    reciver_type?: string;
    image_base64: string;
    conference_time: string;
    have_link: boolean;
}

type ConferenceResponse = {
    id: number;
    sender_id: number;
    sender_type: string;
    receiver_id: number;
    receiver_type: string;
    receiver_name: string;
    content: string;
    image_base64: string | null;
    conference_time: string;
    have_link: boolean;
    created_at: string;
};

const router = useRouter();
const route = useRoute();
const newMessage = ref('');
const messages = ref<ChatMessage[]>([]);
const receiverId = ref<number | undefined>();
const firstName = ref('Неизвестно');
const speciality = ref('');
const lastName = ref('');
const fileInput = ref<HTMLInputElement | null>(null);
const imageUrl = ref<string | null>(null);
const loaded = ref(false);
const isLink = ref(false);
const confTime = ref('');
// Ссылки на сторы пользователя и роли
const roleStore = useRoleStore();
const userStore = useUserStore();
// Получение пользователя по ID и обновление данных
const fetchUserById = async (user_id: number) => {
    try {
        const endpoint = userStore.user?.role !== 'user' ? `/user/get_user/${user_id}` : `/doctor/get_doctor/${user_id}`;
        const user = await api.getData<Patient | Doctor>(endpoint);
        if (user) {
            firstName.value = user.first_name || 'Неизвестно';
            speciality.value = user.speciality || '';
            lastName.value = user.last_name || '';
        }
    } catch (error) {
        console.error('Ошибка при получении пользователя:', error);
    }
};

const sendMessage = async () => {
    if (!newMessage.value.trim() && !imageUrl.value) return;

    const userMessage: ChatMessage = {
        sender_type: 'user',
        text: newMessage.value,
        created_at: new Date().toISOString(),
        image_base64: imageUrl.value || '',
        conference_time: '',
        have_link: false,
    };
    messages.value.push(userMessage);

    try {
        await api.postData('/messages/send', {
            receiver_id: receiverId.value,
            content: newMessage.value,
            image_base64: imageUrl.value || '',
        });

        newMessage.value = '';
        imageUrl.value = '';
        loaded.value = false;
    } catch (error) {
        console.error('Ошибка при отправке сообщения:', error);
    }
};

const fetchMessages = async (receiverId: number) => {
    try {
        const response = await api.getData<Message[]>(`/messages/get_chat/${receiverId}`);
        if (response) {
            messages.value = Object.values(response).map((msg: Message) => ({
                sender_type: msg.sender_type === userStore.user?.role ? 'user' : 'doctor',
                text: msg.content,
                created_at: new Date(new Date(msg.created_at).getTime() + 3 * 60 * 60 * 1000).toISOString(),
                image_base64: msg.image_base64 || '',
                have_link: msg.have_link,
                conference_time: msg.conference_time,
            }));

            isLink.value = response.some((msg: Message) => msg.have_link);
        }
    } catch (error) {
        console.error('Ошибка при получении сообщений:', error);
    }
};

const triggerFileInput = () => {
    console.log('triggerFileInput called');
    fileInput.value?.click();
};

const onFileChange = (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
        const file = target.files[0];
        const reader = new FileReader();

        reader.onload = (e) => {
            imageUrl.value = e.target?.result as string;
        };
        reader.readAsDataURL(file);
        console.log(imageUrl);
        loaded.value = true;
    }

    if (fileInput.value) {
        fileInput.value.value = '';
    }
};

const fetchDateCall = async () => {
    try {
        const response = await api.postData('/messages/conference', {
            receiver_id: receiverId.value,
            conference_time: '2024-11-23T03:03:23.198Z',
        });

        const conferenceData = response as ConferenceResponse;
        isLink.value = conferenceData.have_link;
        confTime.value = conferenceData.conference_time;
        console.log(isLink.value, confTime.value + 'owurihf');
    } catch (error) {
        console.error(error);
    }
};

onMounted(async () => {
    receiverId.value = Number(route.params.id);
    console.log(receiverId.value);
    if (receiverId.value !== undefined) {
        await fetchUserById(receiverId.value);
        await fetchMessages(receiverId.value);
    }
    const interval = setInterval(() => fetchMessages(receiverId.value as number), 5000);
    onUnmounted(() => clearInterval(interval));
});

const goBack = () => {
    router.go(-1);
};

const autoResize = (event: Event) => {
    const textarea = event.target as HTMLTextAreaElement;
    textarea.style.height = '31px';
    textarea.style.height = `${Math.min(textarea.scrollHeight, 110)}px`;
};
</script>

<style lang="scss" scoped>
.videoButtonWrapper {
    position: fixed;
    top: 70px; /* Расстояние от верхнего края, под header */
    left: 50%;
    transform: translateX(-50%);
    z-index: 10; /* Над содержимым сообщений */
    padding: 10px;
    border-radius: 8px; /* Опционально, для стиля */
}

.borderPic {
    margin-bottom: 3px;
    padding-right: 6px;
    padding-left: 3px;
}
.aiChatPage {
    display: flex;
    flex-direction: column;
}
.chatHeader {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 60px;
    background: #fff;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    padding: 0 20px;
    font-family: var(--font-main);
    z-index: 2;
    .icon {
        position: absolute;
        left: 20px;
        top: 50%;
        transform: translateY(-50%);
    }
    .headerText {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0;
        h4 {
            color: var(--Text, #1d1d1d);
            font-size: 18px;
            font-style: normal;
            font-weight: 800;
            line-height: normal;
        }
        p {
            color: rgba(29, 29, 29, 0.5);
            text-align: center;
            font-size: 14px;
            font-style: normal;
            font-weight: 500;
            line-height: normal;
        }
    }
}
.inputBar {
    position: fixed;
    bottom: 0;
    left: 0;
    z-index: 2;
    width: 100%;
    height: auto;
    max-height: 130px;
    padding: 8px 20px 15px 20px;

    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: end;
    background: #fff;

    textarea {
        width: 80%;
        border-radius: 12px;
        background: #f0f0f0;
        padding: 8px 12px;
        min-height: 31px;
        max-height: 110px;
        color: var(--Text, #1d1d1d);
        font-family: var(--font-main);
        font-size: 16px;
        font-style: normal;
        font-weight: 400;
        line-height: normal;
        resize: none; /* Отключает возможность изменения размера вручную */
        overflow: hidden; /* Скрываем прокрутку */
        height: 10px;
        &:focus {
            outline: none;
        }
    }
}

.chatBody {
    z-index: 1;
    width: 100%;
    height: auto;
    padding: 70px 10px 90px 10px;
    overflow-y: auto;

    flex-grow: 1;
    display: flex;
    flex-direction: column;
    font-family: var(--font-main);
    justify-content: flex-end;
    gap: 10px;
    .message {
        display: inline-flex;
        max-width: 80%;
        width: auto;
        overflow-y: scroll;
        padding: 12px 16px;
        align-items: center;
        gap: 10px;
        flex-shrink: 0;
        border-radius: 16px;

        margin-bottom: 10px; /* Пространство между сообщениями */
        z-index: 3;
        backdrop-filter: blur(8px);
        overflow: visible;
        .time {
            color: rgba(29, 29, 29, 0.3);
            font-family: var(--font-main);
            font-size: 12px;
            font-style: normal;
            font-weight: 700;
            line-height: normal;
            z-index: 3;
        }
        .time-doctor {
            position: absolute;
            bottom: -20px;
            left: 0;
        }
        .time-user {
            position: absolute;
            bottom: -20px;
            right: 0;
        }
    }
    .message-user {
        align-self: flex-end; /* Сообщения пользователя справа */
        text-align: right;
        color: #fff;
        border-radius: 16px;
        background: var(--color-main); /* Светлый синий фон для сообщений пользователя */
        border-radius: 30px 0 30px 30px;
    }

    .message-doctor {
        align-self: flex-start; /* Сообщения бота слева */
        text-align: left;
        color: #1d1d1d;
        background: #e9e9e9;
        font-size: 16px;
        font-style: normal;
        font-weight: 400;
        line-height: 150%;
        border-radius: 0 30px 30px 30px;
    }
    .messageImage {
        max-width: 200px;
        max-height: 200px;
        border-radius: 8px;
        margin-top: 8px;
        display: block;
    }

    /* Стили для широких экранов */
    @media screen and (min-width: 1024px) {
        .messageImage {
            max-width: 150px; /* Уменьшаем размеры */
            max-height: 150px;
        }
    }

    .messageBox {
        display: flex;
        flex-direction: column;
        max-width: 150px;
        max-height: 200px;
        text-align: center;
    }

    .imagePreview {
        display: none;
    }
}
</style>
