import React, { useState } from "react";
import { useDropzone } from "react-dropzone";

const DropzoneUploader = ({ onUpload }) => {
  const [files, setFiles] = useState([]);

  const { getRootProps, getInputProps } = useDropzone({
    accept: ".jpg,.jpeg,.png,.webp",
    multiple: true,
    maxFiles: 10,
    onDrop: (acceptedFiles) => {
      const validFiles = acceptedFiles.filter((file) =>
        /\.(jpg|jpeg|png|webp)$/i.test(file.name)
      );

      if (validFiles.length !== acceptedFiles.length) {
        alert("Some files were skipped due to invalid formats.");
      }

      setFiles(validFiles);
      onUpload(validFiles);
    },
  });

  return (
    <div className="border-dashed border-2 border-gray-300 p-4 text-center cursor-pointer">
      <div {...getRootProps()}>
        <input {...getInputProps()} />
        <p>Drag & drop images here, or click to select files</p>
      </div> 
    </div>
  );
};

export default DropzoneUploader;
