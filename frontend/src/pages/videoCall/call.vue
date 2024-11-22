<script setup lang="js">
import { ref, onMounted } from 'vue';

const localStream = ref(null);
const peerConnection = ref(null);
const socket = new WebSocket('ws://skin-cancer.ru:5000');

const localVideo = ref(null);
const remoteVideo = ref(null);

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
};
</script>

<template>
    <div>
        <p>skurh</p>
        <video ref="localVideo" autoplay muted></video>
        <video ref="remoteVideo" autoplay></video>
        <button @click="handleStartCall">Start Call</button>
    </div>
</template>

<style lang="scss" scoped>
video {
    width: 45%;
    margin: 20px;
}
</style>
