import React from "react";

interface InputFieldProps {
  value: string;
  placeholder?: string;
  onChange: (value: string) => void;
}

const InputField: React.FC<InputFieldProps> = ({
  value,
  placeholder,
  onChange,
}) => {
  return (
    <input
      type="text"
      className="border border-gray-300 rounded p-2 w-full"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
    />
  );
};

export default InputField;
