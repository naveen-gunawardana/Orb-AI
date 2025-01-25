import React, { useEffect, useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

const Ripples = () => {
    const groupRef = useRef();
    const audioContextRef = useRef(null);
    const analyserRef = useRef(null);
    const dataArrayRef = useRef(null);
    const animationFrameRef = useRef(null);
    const avgVolumeRef = useRef(0); // To store average volume

    // Initialize audio processing
    useEffect(() => {
        const initAudio = async () => {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                const audioContext = new AudioContext();
                audioContextRef.current = audioContext;

                const source = audioContext.createMediaStreamSource(stream);
                const analyser = audioContext.createAnalyser();
                analyser.fftSize = 256;
                analyserRef.current = analyser;

                source.connect(analyser);
                dataArrayRef.current = new Uint8Array(analyser.frequencyBinCount);

                // Start processing audio
                const processAudio = () => {
                    analyser.getByteFrequencyData(dataArrayRef.current);
                    const avgVolume =
                        dataArrayRef.current.reduce((a, b) => a + b, 0) / dataArrayRef.current.length;
                    avgVolumeRef.current = avgVolume / 256; // Normalize to a range of 0-1
                    animationFrameRef.current = requestAnimationFrame(processAudio);
                };

                processAudio();
            } catch (error) {
                console.error("Error accessing microphone:", error);
            }
        };

        initAudio();

        // Cleanup function
        return () => {
            if (animationFrameRef.current) {
                cancelAnimationFrame(animationFrameRef.current);
            }
            if (audioContextRef.current) {
                audioContextRef.current.close();
            }
        };
    }, []);

    // Create initial ripples
    useEffect(() => {
        if (groupRef.current) {
            for (let i = 0; i < 5; i++) {
                const ring = new THREE.Mesh(
                    new THREE.RingGeometry(1 + i * 0.3, 1.3 + i * 0.3, 32),
                    new THREE.MeshBasicMaterial({
                        color: "cyan",
                        transparent: true,
                        opacity: 1,
                    })
                );
                groupRef.current.add(ring);
            }
        }
    }, []);

    // Animate ripples
    useFrame(() => {
        const avgVolume = avgVolumeRef.current;
        if (groupRef.current) {
            groupRef.current.children.forEach((ring) => {
                ring.scale.x += 0.05 + avgVolume * 2; // Scale dynamically based on volume
                ring.scale.y += 0.05 + avgVolume * 2;
                ring.material.opacity -= 0.01;

                if (ring.material.opacity <= 0) {
                    ring.scale.set(1, 1, 1); // Reset scale
                    ring.material.opacity = 1; // Reset opacity
                }
            });
        }
    });

    return <group ref={groupRef} />;
};

export default Ripples;
