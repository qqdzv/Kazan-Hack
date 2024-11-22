<script setup lang="js">
import MainButton from '@/ui/MainButton.vue';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const localStream = ref(null);
const peerConnection = ref(null);
const socket = new WebSocket('ws://skin-cancer.ru:5000');
const router = useRouter();

const localVideo = ref(null);
const remoteVideo = ref(null);
const calling = ref(false);

// const props = defineProps({
//     docName: String,
//     docQual: String
// })

const config = {
    iceServers: [{ urls: 'stun:stun.l.google.com:19302' }],
};

const startMedia = async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        localStream.value = stream;
        if (localVideo.value) {
            localVideo.value.srcObject = stream;
        }
    } catch (error) {
        console.error('Error accessing media devices.', error);
    }
};

const startCall = () => {
    peerConnection.value = new RTCPeerConnection(config);

    // Отправляем медиапоток на удаленный клиент
    localStream.value.getTracks().forEach((track) => peerConnection.value.addTrack(track, localStream.value));

    // Обработка ICE кандидатов
    peerConnection.value.onicecandidate = (event) => {
        if (event.candidate) {
            socket.send(JSON.stringify({ type: 'ice-candidate', candidate: event.candidate }));
        }
    };

    // Прием видеопотока от удаленного клиента
    peerConnection.value.ontrack = (event) => {
        if (remoteVideo.value) {
            remoteVideo.value.srcObject = event.streams[0];
        }
    };

    // Создание предложения (offer)
    peerConnection.value
        .createOffer()
        .then((offer) => peerConnection.value.setLocalDescription(offer))
        .then(() => {
            socket.send(
                JSON.stringify({
                    type: 'offer',
                    offer: peerConnection.value.localDescription,
                }),
            );
        })
        .catch((error) => {
            console.error('Error creating offer:', error);
        });
};

// Обработка сообщений от сервера сигнализации
socket.onmessage = (event) => {
    const message = JSON.parse(event.data);

    switch (message.type) {
        case 'offer':
            peerConnection.value
                .setRemoteDescription(new RTCSessionDescription(message.offer))
                .then(() => peerConnection.value.createAnswer())
                .then((answer) => peerConnection.value.setLocalDescription(answer))
                .then(() => {
                    socket.send(
                        JSON.stringify({
                            type: 'answer',
                            answer: peerConnection.value.localDescription,
                        }),
                    );
                })
                .catch((error) => {
                    console.error('Error handling offer:', error);
                });
            break;

        case 'answer':
            peerConnection.value.setRemoteDescription(new RTCSessionDescription(message.answer)).catch((error) => {
                console.error('Error setting remote description:', error);
            });
            break;

        case 'ice-candidate':
            peerConnection.value.addIceCandidate(new RTCIceCandidate(message.candidate)).catch((error) => {
                console.error('Error adding ICE candidate:', error);
            });
            break;

        default:
            break;
    }
};

// Старт видеозвонка
const handleStartCall = async () => {
    await startMedia();
    startCall();
    calling.value = true;
};

const endCall = () => {
    router.push('/patient/home').then(() => {
        location.reload();
    });
};
</script>

<template>
    <h4>Хирург Хирургович</h4>

    <div class="video-container" :style="{ marginTop: '30px' }">
        <video ref="localVideo" autoplay muted></video>
        <video ref="remoteVideo" autoplay></video>

        <div class="button-container">
            <MainButton v-if="!calling" @click="handleStartCall" type="primary" text="Подключиться" :width="205"></MainButton>

            <div v-if="calling" :style="{ display: 'flex' }">
                <div :style="{ backgroundColor: '#E1DEDE', padding: '15px', borderRadius: '100%', cursor: 'pointer' }">
                    <img src="/img/videoCall/mute.png" alt="banner_1" />
                </div>

                <div @click="endCall" :style="{ backgroundColor: '#E57676', marginLeft: '25px', marginRight: '25px', padding: '15px', borderRadius: '100%', cursor: 'pointer' }">
                    <img src="/img/videoCall/phone-call-end.png" alt="banner_1" />
                </div>

                <div :style="{ backgroundColor: '#E1DEDE', padding: '15px', borderRadius: '100%', cursor: 'pointer' }">
                    <img src="/img/videoCall/video-off.png" alt="banner_1" />
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.video-container {
    margin-top: 0; /* Убираем отступ сверху */
    display: flex;
    flex-direction: column; /* Располагаем элементы по вертикали */
    justify-content: space-between; /* Равномерное распределение элементов */
    align-items: center;
    height: 100vh; /* Высота контейнера равна высоте экрана */
    gap: 10px;

    /* На мобильных устройствах: */

    @media (min-width: 769px) {
        flex-direction: row; /* Элементы располагаться по горизонтали */
        gap: 10px; /* Отступы между видео */
    }
    @media (max-width: 768px) {
        video {
            width: 100%; /* Видео занимает всю ширину */
            height: calc(33% - 10px); /* Равномерное распределение высоты */
        }

        .button-container {
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            height: calc(33% - 10px); /* Растягиваем кнопку на 1/3 высоты */
        }
    }
}

.video-container video {
    width: 45%; /* Ширина видео по умолчанию */
    max-width: 100%;
    height: auto;
    border: 1px solid #ddd;
    border-radius: 18px;
    background-color: #d2d2d2;

    @media (max-width: 768px) {
        /* На мобильных видео растягиваются */
        width: 100%;
        height: calc(70% - 10px); /* Равномерное распределение по высоте */
    }
}

.button-container {
    display: flex;
    justify-content: center; /* Центрируем по горизонтали */
    align-items: center; /* Центрируем по вертикали */
    width: 100%; /* Растягиваем контейнер на всю ширину */
    height: 50px; /* Высота кнопки */
    background-color: transparent; /* Прозрачный фон */

    /* Медиазапрос для мобильных устройств */
    @media (max-width: 768px) {
        justify-content: stretch; /* Растягиваем дочерние элементы */
        padding: 0 10px; /* Добавляем небольшой отступ */

        button {
            width: 100%; /* Растягиваем кнопку на всю ширину */
        }
    }
}

p {
    color: rgba(29, 29, 29, 0.5);
    font-family: var(--font-main);
    font-size: 12px;
    font-style: normal;
    font-weight: 500;
    line-height: normal;
}
h4 {
    color: var(--Text, #1d1d1d);
    font-size: 18px;
    font-style: normal;
    font-weight: 800;
    line-height: normal;
}
</style>
