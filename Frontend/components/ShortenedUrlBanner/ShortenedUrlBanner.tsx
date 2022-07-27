import React, { useState } from 'react'
import useCopyToClipboard from '../../hooks/useCopyToClipboard'

interface IProps {
    shortenedUrl: string
}

const ShortenedUrlBanner = ({ shortenedUrl }: IProps) => {
    const [copiedText, copy] = useCopyToClipboard()
    const [timeout, setTime] = useState<null | NodeJS.Timeout>(null)
    const [showTooltip, setShowTooltip] = useState(false)

    const handleClick = () => {
        setShowTooltip(true)
        copy(shortenedUrl)
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
        <div className='border-solid border-[1px] bg-[#FAFBFB] rounded-[8px]  px-2 md:px-4 pt-2 md:pt-1 py-1 w-full md:max-w-max relative md:flex items-center gap-2 max-w-lg mx-auto md:mx-w-none'>
            <p className='text-sm flex-grow md:inline-block mb-2 md:mb-0  font-semibold'>Here you go:</p>

            <div className='flex flex-col  md:flex-row space-y-2 md:space-y-0 md:space-x-2 md:items-center'>


                <p className='text-base p-2 bg-white  text-[#2B7FFF]'>{shortenedUrl}</p>
                <button className='inline-block  relative top-1/2 text-[#6B788E] hover:text-inherit p-2 self-end' onClick={() => handleClick()}>
                    {showTooltip && <span className='absolute -left-[130%] md:-left-0 -top-5 bg-gray-400 text-[#fefefe] p-1 text-[12px] w-[120px]'>URL copied already</span>}
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                </button>
            </div>
        </div>
    )
}

export default ShortenedUrlBanner