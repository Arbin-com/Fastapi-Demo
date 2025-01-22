import React from "react";

interface DropdownProps {
  options: { value: string; status?: number }[];
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
      <option value="" key="" disabled>
        Select an option
      </option>
      {options.map((option, index) => (
        <option
          key={index}
          value={option.value}
          disabled={
            option.status !== undefined && ![0, 15].includes(option.status)
          }
          className={`flex items-center justify-between px-4 py-2 ${
            option.status == undefined ||
            (option.status !== undefined && [0, 15].includes(option.status))
              ? ""
              : "bg-gray-300 text-gray-500"
          }`}
        >
          {option.status !== undefined
            ? `Channel ${option.value + 1}`
            : option.value}
        </option>
      ))}
    </select>
  );
};

export default Dropdown;
