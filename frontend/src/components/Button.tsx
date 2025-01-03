import React from "react";

interface ButtonProps {
  label: string;
  disabled?: boolean;
  onClick: () => void;
}

const Button: React.FC<ButtonProps> = ({ label, disabled, onClick }) => {
  return (
    <button
      className={`bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 ${
        disabled ? "opacity-50 cursor-not-allowed" : ""
      }`}
      disabled={disabled}
      onClick={onClick}
    >
      {label}
    </button>
  );
};

export default Button;
