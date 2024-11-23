<template>
    <header class="header">
        <!-- <CustomIcon id="logo" :width="207" :height="33" className="logo" @click="router.push('/' + role.role + '/home')" /> -->
        <div @click="router.back()" :style="{ display: 'flex', marginTop: '10px' }">
            <img src="/img/homepage/faceIcon.png" alt="" class="src" />
            <h2 :style="{ marginLeft: '10px', marginTop: '3px' }">TeleDoc</h2>
        </div>
        <div class="subNavGroup">
            <CustomIcon id="notification" :width="28" :height="28" @click="turnNotificationOn" />
            <CustomIcon id="settings" :width="28" :height="28" @click="router.push('/settings')" />
        </div>
    </header>
</template>

<script setup lang="ts">
import { useRoleStore } from '@/store/useRoleStore';
import { useUserStore } from '@/store/useUserStore';
import CustomIcon from '@/ui/CustomIcon.vue';
import { useRouter } from 'vue-router';

// Get the role store
const role = useRoleStore();
const router = useRouter();

const turnNotificationOn = () => {
    window.open(`https://t.me/teledoc_ntf_bot?start=${useUserStore().user?.id}`, '_blank');
};
</script>

<style lang="scss">
h2 {
    color: var(--Text, #16c4a4);
    font-family: var(--font-main);
    font-size: 20px;
    font-style: normal;
    font-weight: 600;
    line-height: normal;
}
.header {
    width: 100%;

    position: fixed;
    top: 0;
    left: 0;
    z-index: 3;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    padding: 10px 20px;
    animation: fadeIn 0.5s ease-in-out forwards;
    background-color: #fafafa;
    .subNavGroup {
        display: flex;
        flex-direction: row;
        gap: 28px;
    }
}
@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
</style>
