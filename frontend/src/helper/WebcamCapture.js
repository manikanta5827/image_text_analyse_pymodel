import React, { useRef, useState, useEffect } from "react";
import Webcam from "react-webcam";  
import cv from 'opencv.js';

const WebcamCapture = ({ onCapture }) => {
    const webcamRef = useRef(null);
    const [isCapturing, setIsCapturing] = useState(false);

    useEffect(() => {
        if (typeof cv === 'undefined') {
            alert("OpenCV.js not loaded correctly");
        }
    }, []);

    const captureImage = async () => {
        if (isCapturing) return;
        setIsCapturing(true);

        const imageSrc = webcamRef.current.getScreenshot();
        if (!imageSrc) {
            setIsCapturing(false);
            return;
        }

        const img = new Image();
        img.src = imageSrc;
        img.onload = async () => {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);

            let src = cv.imread(canvas);
            let dst = new cv.Mat();
            let edges = new cv.Mat();

            cv.cvtColor(src, src, cv.COLOR_RGBA2GRAY, 0);
            cv.Canny(src, edges, 50, 100, 3, false);

            const nonZero = cv.countNonZero(edges);
            if (nonZero > 1000) {
                await processCapture(src);
            }

            src.delete();
            dst.delete();
            edges.delete();
            setIsCapturing(false);
        };
    };

    const processCapture = async (src) => {
        const canvas = document.createElement('canvas');
        cv.imshow(canvas, src);
        const base64Image = canvas.toDataURL("image/png");

        const response = await fetch(base64Image);
        const blob = await response.blob();
        const file = new File([blob], `captured_${new Date().toISOString()}.png`, { type: "image/png" });

        onCapture(file);
    };

    return (
        <div className="flex flex-col items-center">
            <Webcam
                ref={webcamRef}
                screenshotFormat="image/png"
                className="w-64 h-48 border rounded shadow"
                mirrored={false}
                videoConstraints={{
                    facingMode: "user",
                }}
            />
            <button
                className="bg-blue-500 text-white px-4 py-2 mt-2 rounded"
                onClick={captureImage}
                disabled={isCapturing}
            >
                {isCapturing ? "Capturing..." : "Capture Image"}
            </button>
        </div>
    );
};

export default WebcamCapture;
