import React from "react";

interface DropdownProps {
  options: { value: string; status?: string }[];
  selected: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

const Dropdown: React.FC<DropdownProps> = ({
  options,
  selected,
  onChange,
  disabled,
}) => {
  return (
    <select
      value={selected}
      disabled={disabled}
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
          disabled={option.status && option.status !== "Idle" ? true : false}
          className={`${
            option.status && option.status != "Idel"
              ? "bg-gray-300 text-gray-500"
              : ""
          }`}
        >
          {option.value}
          {option.status}
        </option>
      ))}
    </select>
  );
};

export default Dropdown;
