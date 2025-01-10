import React from "react";

interface DropdownProps {
  options: { value: string; label?: string; disabled?: boolean }[];
  selected: string;
  onChange: (value: string) => void;
}

const Dropdown: React.FC<DropdownProps> = ({ options, selected, onChange }) => {
  return (
    <select
      value={selected}
      onChange={(e) => onChange(e.target.value)}
      className="w-full p-2 border rounded"
    >
      <option value="" disabled>
        Select an option
      </option>
      {options.map((option) => (
        <option
          key={option.value}
          value={option.value}
          disabled={option.disabled}
          className={`${option.disabled ? "bg-gray-300 text-gray-500" : ""}`}
        >
          {option.label}
        </option>
      ))}
    </select>
  );
};

export default Dropdown;
