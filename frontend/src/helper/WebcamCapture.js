import React, { useRef, useState } from "react";
import Webcam from "react-webcam";

const WebcamCapture = ({ onCapture }) => {
    const webcamRef = useRef(null);

    const captureImage = async () => {
        const imageSrc = webcamRef.current.getScreenshot();
        if (!imageSrc) return;

        // Convert base64 to File
        const response = await fetch(imageSrc);
        const blob = await response.blob();
        const file = new File([blob], `captured_${new Date().getFullYear()}.${new Date().getMonth()+1}.${new Date().getDate()}.png`, { type: "image/png" });

        onCapture(file);
    };

    return (
        <div className="flex flex-col items-center">
            <Webcam
                ref={webcamRef}
                screenshotFormat="image/png"
                className="w-64 h-48 border rounded shadow"
                mirrored={false} // Fixes the mirror issue
                videoConstraints={{
                    facingMode: "user", // Use front camera by default
                }}
            />
            <button
                className="bg-blue-500 text-white px-4 py-2 mt-2 rounded"
                onClick={captureImage}
            >
                Capture Image
            </button>
        </div>
    );
};

export default WebcamCapture;
