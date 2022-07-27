import React from 'react'
interface IProps {
    color?: string
}
const Loader = ({ color }: IProps) => {
    return (
        <div className={`mx-auto container w-[75px] h-[15px] items-center flex relative`}>
            <span className={`circle absolute top-0 left-0 animate-grow ${color}`}></span>
            <span className={`circle ${color}`}></span>
            <span className={`circle ${color}`}></span>
            <span className={`circle absolute top-0 right-0 mr-0 animate-grow ${color}`}></span>
        </div>
    )
}

export default Loader