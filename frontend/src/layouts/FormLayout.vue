<template>
    <div class="formLayout">
        <!-- <CustomIcon id="logo" :width="207" :height="33" className="logo" /> -->
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
            <img src="/img/homepage/faceIcon.png" alt="" style="width: 40px; height: 40px" />
            <h2 :style="{ marginLeft: '5px', marginTop: '0' }">TeleDoc</h2>
        </div>
        <router-view />
    </div>
</template>

<script setup lang="ts">
import CustomIcon from '@/ui/CustomIcon.vue';
defineOptions({
    name: 'FormLayout',
});
</script>

<style scoped lang="scss">
h2 {
    color: var(--Text, #16c4a4);
    font-family: var(--font-main);
    font-size: 32px;
    font-style: normal;
    font-weight: 600;
    line-height: normal;
}
.formLayout {
    width: 100%;
    padding-top: 36px;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100dvh;
    .logo {
        position: relative;
        width: 207px;
        height: 33px;
        z-index: 6;
    }
}
</style>
