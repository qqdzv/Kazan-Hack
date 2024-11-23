<template>
    <div class="step4">
        <h2 v-if="!show">Что вы хотите отсканировать?</h2>

        <div v-if="!show" :style="{ display: 'flex', marginTop: '40px' }">
            <MainButton text="Родинку" @click="selectAnswer('Родинку')" :class="{ active: selectedOption === 'Родинку' }" type="secondary" />

            <MainButton
                :style="{ marginLeft: '30px' }"
                text="Кожу"
                @click="
                    selectAnswer('кожу');
                    triggerFileInput();
                "
                :class="{ active: selectedOption === 'кожу' }"
                type="secondary"
            />
        </div>

        <h4 v-if="loading" class="text-center" :style="{ marginTop: '50px' }">Загрузка...</h4>

        <TestResult v-if="show" :folder_name="folder_name" :image_base64="image_base64" />
    </div>
    <div class="bottom">
        <MainButton text="Назад" @click="router.go(-1)" type="secondary" />

        <MainButton v-if="!show" text="Далее" @click="nextStep" type="primary" />
    </div>

    <input type="file" accept="image/*" ref="fileInput" class="hidden" :style="{ opacity: '0' }" @change="onFileChange" />
</template>

<script setup lang="ts">
import { defineProps, defineEmits, ref, watch } from 'vue';
import MainButton from '@/ui/MainButton.vue';
import { useRouter } from 'vue-router';
import api from '@/axios/api';
import TestResult from './TestResult.vue';

const selectedOption = ref<string | null>(''); // Храним выбранный вариант
const fileInput = ref<HTMLInputElement | null>(null);
const imageUrl = ref<string | null>(null);
const router = useRouter();
const loading = ref(false);

defineOptions({
    name: 'TestStep4',
});

const props = defineProps<{ task4?: string }>();
const emit = defineEmits(['next-step', 'update:task4', 'prev-step']);
const task4Value = ref(props.task4 || '');
const folder_name = ref('');
const image_base64 = ref('');
const show = ref(false);

interface ScanResponse {
    response: string;
    image_base64: string;
}

watch(task4Value, (newAnswer) => {
    emit('update:task4', newAnswer);
});

const selectAnswer = (task: string) => {
    selectedOption.value = task;
    task4Value.value = task;
};

const nextStep = () => {
    if (task4Value.value === 'кожу') {
        sendSkinPhoto();
    } else {
        if (task4Value.value) {
            emit('next-step');
        }
    }
};

const sendSkinPhoto = async () => {
    loading.value = true;

    try {
        const rawResponse = await api.postData('/scan/send_skin', {
            folder_name: 'Мои сканы',
            image_base64: imageUrl.value,
        });

        const response = rawResponse as ScanResponse;

        folder_name.value = response.response;
        image_base64.value = response.image_base64;

        // router.push('/testResult');
        show.value = true;
    } catch (error) {
        console.error('Ошибка при отправке фото:', error);
    }
    loading.value = false;
};

const triggerFileInput = () => {
    // console.log('triggerFileInput called');
    loading.value = true;
    fileInput.value?.click();
    loading.value = false;
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
    }

    if (fileInput.value) {
        fileInput.value.value = '';
    }
};
</script>

<style lang="scss" scoped>
.text-center {
    text-align: center; /* Выравниваем текст по центру */
    color: var(--Text, #1d1d1d);
    font-size: 18px;
    font-weight: 800;
    line-height: 1.2;
    font-family: var(--font-main);
}
.active {
    background-color: #16c4a4; /* Зеленый цвет для выбранной кнопки */
    color: white; /* Белый текст */
}
.step4 {
    display: flex;
    flex-direction: column;
    gap: 8px;
    width: 100%;
    height: 100%;
    align-items: center;
    margin-top: 10rem;
    .groupBtns {
        display: flex;
        flex-direction: column;
        width: 100%;
        justify-content: space-between;
        gap: 8px;
    }
    h2 {
        color: var(--Text, #1d1d1d);
        font-family: var(--font-main);
        font-size: 32px;
        font-style: normal;
        font-weight: 600;
        line-height: normal;
    }
}
.bottom {
    position: fixed;
    width: 89.7435897vw;
    bottom: 30px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}
</style>
