import React, { useState } from "react";
import axios from "axios";
import ImageUploader from "./components/ImageUploader";
import Loading from "./components/Loading";
import ResultDisplay from "./components/ResultDisplay";

function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleImageUpload = async (files, includeDetails) => {
    setLoading(true);

    const formData = new FormData();
    files.forEach((file) => formData.append("images", file)); // react-dropzone ensures this is an array
    formData.append("includeDetails", includeDetails);

    try {
      const response = await axios.post("http://localhost:4000/api/food-data", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      typeof response.data === "string" ? setResult(JSON.parse(response.data)) : setResult(response.data);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4 ">
      <h1 className="text-3xl font-bold mb-4">FoodAI Image Processing</h1>
      <ImageUploader onImageUpload={handleImageUpload} />
      {loading && <Loading />}
      {result && <ResultDisplay result={result} />}
    </div>
  );
}

export default App;
