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
      <option value="" disabled>
        Select an option
      </option>
      {options.map((option) => (
        <option
          key={option.value}
          value={option.value}
          disabled={option.status !== undefined && option.status !== 0}
          className={`flex items-center justify-between px-4 py-2 ${
            option.status == undefined ||
            (option.status !== undefined && option.status === 0)
              ? ""
              : "bg-gray-300 text-gray-500"
          }`}
        >
          <div className="bg-red-150">
            {option.status !== undefined
              ? option.value
              : `Channel ${option.value + 1}`}
          </div>
        </option>
      ))}
    </select>
  );
};

export default Dropdown;
