import React from 'react'

const Skeleton = ({className}: {className: string}) => {
  return (
    <span className={`bg-[#EBEDF0] animate-pulse inline-block ${className}`}></span>
  )
}

export default Skeleton