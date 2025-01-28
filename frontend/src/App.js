import React, { useState } from "react";
import axios from "axios";
import ImageUploader from "./components/ImageUploader";
import ResultDisplay from "./components/ResultDisplay";

function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleImageUpload = async (files, includeDetails) => {
    setLoading(true);
    setResult(null); // Clear previous result on new upload

    const formData = new FormData();
    files.forEach((file) => formData.append("images", file));
    formData.append("includeDetails", includeDetails);

    try {
      const response = await axios.post("http://127.0.0.1:5000/api/food-data", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setResult(response.data); // Store backend response for display
    } catch (error) {
      console.error("Error uploading images:", error);
      alert("Error processing images. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4 text-red-300">Image Uploader</h1>
      <ImageUploader onImageUpload={handleImageUpload} />
      {loading && <p className="text-blue-500">Uploading and processing...</p>}
      {result && <ResultDisplay result={result} />}
    </div>
  );
}

export default App;
