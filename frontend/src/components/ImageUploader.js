import React, { useState } from "react";
import DropzoneUploader from "../helper/DropzoneUploader";
import WebcamCapture from "../helper/WebcamCapture";

const ImageUploader = ({ onImageUpload }) => {
  const [includeDetails, setIncludeDetails] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);

  const handleDropzoneUpload = (files) => {
    const updatedFiles = files.map((file, index) => ({
      file,
      name: `dropzone_image_${uploadedFiles.length + index + 1}.png`,
    }));
    setUploadedFiles((prev) => [...prev, ...updatedFiles]);
  };

  const handleWebcamUpload = (file) => {
    setUploadedFiles((prev) => [
      ...prev,
      { file, name: file.name },
    ]);
  };

  const handleDeleteImage = (index) => {
    setUploadedFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const handleUploadAll = () => {
    if (uploadedFiles.length === 0) {
      alert("No images selected for upload.");
      return;
    }
    onImageUpload(uploadedFiles.map((item) => item.file), includeDetails);
  };

  return (
    <div>
      <h2 className="text-lg font-bold mb-2">Upload from Device</h2>
      <DropzoneUploader onUpload={handleDropzoneUpload} />

      <h2 className="text-lg font-bold mt-4 mb-2">Capture from Webcam</h2>
      <WebcamCapture onCapture={handleWebcamUpload} />

      <label className="flex items-center space-x-2 mt-4">
        <input
          type="checkbox"
          checked={includeDetails}
          onChange={(e) => setIncludeDetails(e.target.checked)}
        />
        <span>Include Details</span>
      </label>

      <h2 className="text-lg font-bold mt-4">Selected Images</h2>
      <div className="mt-2 grid grid-cols-8 gap-4">
        {uploadedFiles.map((item, index) => (
          <div key={index} className="bg-gray-300 p-2 rounded shadow">
            <img
              src={URL.createObjectURL(item.file)}
              alt={item.name}
              className="w-40 h-40 object-cover"
            />
            <p className="text-sm mt-1">{item.name}</p>
            <button
              className="bg-red-500 text-white text-xs px-2 py-1 rounded mt-1"
              onClick={() => handleDeleteImage(index)}
            >
              Delete
            </button>
          </div>
        ))}
      </div>

      {/* Upload All Images Button */}
      <button
        className="bg-green-500 text-white px-4 py-2 mt-4 rounded w-full"
        onClick={handleUploadAll}
      >
        Upload All Images
      </button>
    </div>
  );
};

export default ImageUploader;
