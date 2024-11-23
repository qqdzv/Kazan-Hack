<template>
    <div class="loader">
        <!-- <CustomIcon id="bigLogo" :width="293" :height="135" /> -->
        <div
            :style="{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                marginTop: '10px',
                width: '207px',
                height: '33px',
            }"
        >
            <img src="/img/homepage/faceIcon.png" alt="" style="width: 30px; height: 30px" />
            <h2 :style="{ marginLeft: '5px', marginTop: '0' }">TeleDoc</h2>
        </div>
        <div class="circle" :class="{ animate: isAnimating }" />
    </div>
</template>

<script setup lang="ts">
import CustomIcon from '@/ui/CustomIcon.vue';
import { ref, onMounted } from 'vue';

defineOptions({
    name: 'Loader',
});

const isAnimating = ref(false);

// Запускаем анимацию после монтирования компонента
onMounted(() => {
    isAnimating.value = true;
});
</script>

<style lang="scss">
h2 {
    color: var(--Text, #16c4a4);
    font-family: var(--font-main);
    font-size: 32px;
    font-style: normal;
    font-weight: 600;
    line-height: normal;
}
.loader {
    width: 100%;
    height: 100dvh;
    margin-top: 209px;
    overflow: hidden; /* Скрыть переполнение */
    display: flex;
    flex-direction: column;
    align-items: center;
    touch-action: manipulation;
    .circle {
        position: absolute;
        bottom: 0;
        left: 25%; /* Центрирование по горизонтали */
        width: 200px; /* Начальный размер круга */
        height: 200px; /* Начальный размер круга */
        border-radius: 50%; /* Делает элемент кругом */
        background: #16c4a4;
        transition: all 0.5s ease; /* Плавное изменение свойств */
        transform: translateX(-25%);
        touch-action: manipulation;
    }
}

.animate {
    animation:
        jump 2s forwards,
        jump 2s 2s forwards,
        expand 1s 4s forwards; /* Запускаем анимации */
}

@keyframes jump {
    0% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-150px); /* Прыжок вверх */
    }
    100% {
        transform: translateY(0);
    }
}

@keyframes expand {
    0% {
        width: 200px; /* Начальный размер */
        height: 200px; /* Начальный размер */
    }
    100% {
        width: 1000px; /* Заполняем ширину экрана */
        height: 1000px; /* Заполняем высоту экрана */
        bottom: 0; /* Позиция внизу */
        transform: translateX(-25%);
        border-radius: 300px;
    }
}
</style>
