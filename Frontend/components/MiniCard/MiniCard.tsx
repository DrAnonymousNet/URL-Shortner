import React, { useState } from 'react'
import useCopyToClipboard from '../../hooks/useCopyToClipboard'
import Skeleton from '../Skeleton/Skeleton'

interface IMiniCard {
    property: string,
    value: string,
    isLoading: boolean
    colored?: boolean
    underline?: boolean
    truncate?: boolean
    

}

const MiniCard = ({ property, value, isLoading , underline, truncate , colored = false}: IMiniCard) => {


    const [copiedText, copy] = useCopyToClipboard()
    const [timeout, setTime] = useState<null | NodeJS.Timeout>(null)
    const [showTooltip, setShowTooltip] = useState(false)
  
    const handleClick = () => {
        setShowTooltip(true)
        copy(value)
        setTime(
            setTimeout(() => {
                setShowTooltip(false)
            }, 500)
        )
        if (timeout) {
            return () => clearTimeout(timeout)
        }
    }
  
  



    return (
        <div className='text-[15px] py-2 md:px-4 flex flex-wrap items-baseline  '>
            <p className='font-semibold  inline-block  mr-1  tracking-wide'>
                {property}:
            </p>
            {
                isLoading ?
                    <Skeleton className='block w-full h-4' /> :
                    (
                    underline ? 
                    <p className={`${colored ? "text-blue-600" : ""} ${truncate ? " truncate" : ""} cursor-pointer inline-block relative underline underline-offset-2 py-[6px]`} onClick={() =>handleClick()} >
                     {showTooltip && <div className=' absolute  -top-[-0.1rem] bg-gray-400 text-[#fefefe] p-1 block text-[12px] w-[120px] right-0'>URL copied already</div>}
                   

                    {/* <a href={value} target="_blank"> */}
                        {value}
                    {/* </a> */}
                    </p>
                     :
                    <span className={` text-[14px] tracking-wide `}>

                        {value}
                    </span>
                    )
            }
        </div >
    )
}

export default MiniCard