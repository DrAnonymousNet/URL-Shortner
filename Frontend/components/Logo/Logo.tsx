import Link from 'next/link'
import React from 'react'

const Logo = () => {
    return (
        <Link href="/" >

            <div className='flex items-center cursor-pointer '>
                <span>

                    <svg width="32" height="48" viewBox="0 0 40 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M16 20V14C16 9.58172 19.5817 6 24 6V6C28.4183 6 32 9.58172 32 14V20" stroke="#0B1A30" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        <path d="M24 32L24 16" stroke="#0047B3" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        <path d="M16 28V34C16 38.4183 19.5817 42 24 42V42C28.4183 42 32 38.4183 32 34V28" stroke="#0B1A30" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                </span>
                <p className='text-base font-black tracking-wider '>
                    SHORTEN<span className='text-[#2B7FFF]'>R</span>
                </p>



            </div>
        </Link>
    )
}

export default Logo