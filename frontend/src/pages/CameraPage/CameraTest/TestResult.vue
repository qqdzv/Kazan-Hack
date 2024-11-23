<script setup lang="ts">
const props = defineProps<{
    folder_name: string;
    image_base64: string;
}>();
</script>

<template>
    <div class="mainLayout">
        <div class="content-wrapper">
            <div class="circlePhoto">
                <img :src="image_base64" alt="banner_1" />
            </div>

            <h4 class="text-center">{{ props.folder_name }}</h4>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.mainLayout {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100dvh;
    padding: 30px 20px 72px 20px;
}

.content-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center; /* Центрируем элементы по горизонтали */
    justify-content: center; /* Центрируем по вертикали (если понадобится) */
    gap: 10px; /* Расстояние между кругом и текстом */
}

.circlePhoto {
    width: 152px; /* Фиксированная ширина */
    height: 152px; /* Фиксированная высота */
    padding: 3px;
    border: 2px solid;
    border-radius: 50%; /* Круг */
    border-color: #16c4a4;
    display: flex;
    align-items: center; /* Центрируем содержимое */
    justify-content: center;

    img {
        width: 100%; /* Изображение заполняет круг */
        height: 100%;
        object-fit: cover; /* Обрезаем изображение, чтобы заполнить круг */
        border-radius: 50%; /* Закругляем изображение */
    }
}

.text-center {
    text-align: center; /* Выравниваем текст по центру */
    color: var(--Text, #1d1d1d);
    font-size: 18px;
    font-weight: 800;
    line-height: 1.2;
    font-family: var(--font-main);
}

.circlePhoto {
    width: 152px; /* Фиксированная ширина */
    height: 152px; /* Фиксированная высота */
    padding: 3px;
    border: 2px solid;
    border-radius: 50%; /* Закругляем до круга */
    border-color: #16c4a4;
    display: flex; /* Центрируем содержимое */
    align-items: center;
    justify-content: center;

    img {
        width: 100%; /* Ширина изображения равна контейнеру */
        height: 100%; /* Высота изображения равна контейнеру */
        object-fit: cover; /* Обрезаем изображение, чтобы оно заполнило круг */
        border-radius: 50%; /* Устанавливаем круглую форму для изображения */
    }
}

.mainLayout {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100dvh;
    padding: 30px 20px 72px 20px;
}

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
            height: 100%;
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
