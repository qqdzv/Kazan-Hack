<template>
    <!-- <div class="step6">
        <h2>Принимали ли вы какие-либо лекарства в течение последних двух недель?</h2>
        <div class="groupBtns">
            <MainButton text="Нет" :key="task6Value === false ? 'male-button' : 'base-male'" @click="selectAnswer(false)" :type="task6Value === false ? 'primary' : 'base'" :width="165" />
            <MainButton text="Да" @click="selectAnswer(true)" :key="task6Value === true ? 'male-button' : 'base-male'" :type="task6Value === true ? 'primary' : 'base'" :width="165" />
        </div>
    </div> -->
    <div class="bottom">
        <MainButton text="Назад" @click="prevStep" type="secondary" />
        <MainButton text="Далее" @click="nextStep" type="primary" />
    </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, ref, watch } from 'vue';
import MainButton from '@/ui/MainButton.vue';

defineOptions({
    name: 'TestStep6',
});

const props = defineProps<{ task6?: boolean }>();
const emit = defineEmits(['next-step', 'update:task6', 'prev-step']);
const task6Value = ref(props.task6 || false);

watch(task6Value, (newAnswer) => {
    emit('update:task6', newAnswer);
});

const selectAnswer = (task: boolean) => {
    task6Value.value = task;
};

const nextStep = () => {
    emit('next-step');
};

const prevStep = () => {
    emit('prev-step');
};
</script>

<style lang="scss" scoped>
.step6 {
    display: flex;
    flex-direction: column;
    gap: 48px;
    width: 100%;
    height: 100%;
    .groupBtns {
        display: flex;
        flex-direction: row;
        width: 100%;
        justify-content: space-between;
        row-gap: 10px;
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
    bottom: 50px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}
</style>
