// Orb.js

import React, { useEffect, useRef } from "react";
import "./Orb.css"; // Ensure this file defines the .rainbow class

const Orb = () => {
    const orbRef = useRef(null);
    const audioContextRef = useRef(null);
    const analyserRef = useRef(null);
    const dataArrayRef = useRef(null);
    const animationFrameRef = useRef(null);

    useEffect(() => {
        const orb = orbRef.current;
        if (!orb) return;

        // Function to activate the rainbow effect
        const activateRainbow = () => {
            if (!orb.classList.contains("rainbow")) {
                orb.classList.add("rainbow");
            }
        };

        // Function to deactivate the rainbow effect
        const deactivateRainbow = () => {
            if (orb.classList.contains("rainbow")) {
                orb.classList.remove("rainbow");
            }
        };

        // Function to process audio data continuously
        const processAudio = () => {
            if (!analyserRef.current) return;

            analyserRef.current.getByteFrequencyData(dataArrayRef.current);
            const avgVolume = dataArrayRef.current.reduce((a, b) => a + b, 0) / dataArrayRef.current.length;

            if (avgVolume > .2) { // Adjust threshold as needed
                activateRainbow();
            } else {
                deactivateRainbow();
            }

            animationFrameRef.current = requestAnimationFrame(processAudio);
        };

        // Initialize AudioContext and start audio monitoring
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
                processAudio();

                // Handle AudioContext state changes
                audioContext.onstatechange = () => {
                    if (audioContext.state === 'suspended') {
                        audioContext.resume().catch(() => {
                            console.warn("AudioContext resume failed.");
                        });
                    }
                };
            } catch (error) {
                console.error("Error accessing microphone:", error);
            }
        };

        initAudio();

        // Cleanup function to stop audio monitoring and clean up resources
        return () => {
            if (animationFrameRef.current) {
                cancelAnimationFrame(animationFrameRef.current);
            }
            if (analyserRef.current) {
                analyserRef.current.disconnect();
            }
            if (audioContextRef.current) {
                audioContextRef.current.close();
            }
            deactivateRainbow();
        };
    }, []);

    // Click handler to manually resume AudioContext if it's suspended
    const handleOrbClick = () => {
        const audioContext = audioContextRef.current;
        if (audioContext && audioContext.state === 'suspended') {
            audioContext.resume().catch(() => {
                console.warn("AudioContext resume failed on orb click.");
            });
        }
    };

    return (
        <div className="orb-container">
            <div 
                className="ominous-orb" 
                ref={orbRef} 
                onClick={handleOrbClick} 
                style={{ cursor: 'pointer' }} // Indicates interactivity
            ></div>
        </div>
    );
};

export default Orb;
