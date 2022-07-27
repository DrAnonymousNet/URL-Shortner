
interface IOtherAnalytics {
    [key: string]: number
}

export const processOtherAnalytics = (analytics: IOtherAnalytics) => {
    //an empty analytics object , ejects empty array ;) GIGO simply
    if(JSON.stringify({}) === JSON.stringify(analytics)) return []

    const analytics_array = Object.keys(analytics).map(key => ({label: key, value: analytics[key]}))
    let sorted_analytics = analytics_array.sort((a,b) => b.value - a.value)

    if(sorted_analytics.length > 5) sorted_analytics = sorted_analytics.slice(0,6)

    const labels = sorted_analytics.map(obj => obj.label)
    const values = sorted_analytics.map(obj => obj.value)

    return [labels,values] 
}