import React, { useState, useEffect } from "react";
import { useDropzone } from "react-dropzone";

const ImageUploader = ({ onImageUpload }) => {
  const [includeDetails, setIncludeDetails] = useState(false);
  const [files, setFiles] = useState([]);

  const { getRootProps, getInputProps } = useDropzone({
    accept: ".jpg,.jpeg,.png,.webp",
    multiple: true,
    maxFiles: 10,
    onDrop: (acceptedFiles) => {
      // Validate each file before adding to the list
      const validFiles = acceptedFiles.filter((file) =>
        /\.(jpg|jpeg|png|gif)$/i.test(file.name)
      );

      if (validFiles.length !== acceptedFiles.length) {
        alert("Some files were skipped due to invalid file extensions.");
      }

      setFiles(validFiles);
    },
  });

  const handleSubmit = () => {
    if (files.length > 0) {
      onImageUpload(files, includeDetails);
    } else {
      alert("Please select at least one image.");
    }
  };

  // Effect to listen for 'Enter' key press
  useEffect(() => {
    const handleKeyPress = (e) => {
      if (e.key === "Enter") {
        handleSubmit();
      }
    };

    window.addEventListener("keydown", handleKeyPress);

    // Clean up the event listener when the component unmounts
    return () => {
      window.removeEventListener("keydown", handleKeyPress);
    };
  }, [files, includeDetails]); // Dependencies to reattach event listener when files or includeDetails change

  return (
    <div>
      <div
        {...getRootProps()}
        className="border-dashed border-2 border-gray-300 p-4 text-center cursor-pointer"
      >
        <input {...getInputProps()} />
        <p>Drag & drop images here, or click to select files</p>
      </div>
      {files.length > 0 && (
        <ul className="mt-2">
          {files.map((file, idx) => (
            <li key={idx} className="text-sm">
              {file.name}
            </li>
          ))}
        </ul>
      )}
      <div className="mt-4">
        <label className="flex items-center space-x-2">
          <input
            type="checkbox"
            checked={includeDetails}
            onChange={(e) => setIncludeDetails(e.target.checked)}
          />
          <span>Include Details</span>
        </label>
        <button
          onClick={handleSubmit}
          className="bg-blue-500 text-white px-4 py-2 mt-4 rounded"
        >
          Upload
        </button>
      </div>
    </div>
  );
};

export default ImageUploader;
