import React from 'react'

interface IProps {
    children: JSX.Element | string
}

const ListItem: React.FC<IProps> = ({ children }) => {
    return (
        <li className='flex gap-1 items-center'>
            <span className='inline-block'>
                <svg width="16" height="17" viewBox="0 0 16 17" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="8" cy="8.5" r="5" fill="#E6F0FF" />
                    <circle cx="7.99996" cy="8.5" r="2" fill="#091E42" />
                </svg>




            </span>
            <p className='text-[14px] w-full font-regular '>
                {children}
            </p>

        </li>
    )
}

export default ListItem