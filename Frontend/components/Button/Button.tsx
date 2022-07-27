import React from 'react'

interface Props {
    classname?: string,
    disabled?: boolean,
    onClick?:  (e: React.FormEvent) => void
    children: string | JSX.Element
}

const Button: React.FC<Props> = ({children,classname , disabled = false , onClick} ) => {
    return (
        <button className={`text-[#fff] outline-none py-3 w-full block hover:opacity-80 focus:opacity-80 focus:outline-1 font-bold rounded-lg disabled:opacity-50  ${classname}`} disabled={disabled} onClick={onClick}>
            {children}
        </button>
    )
}

export default Button