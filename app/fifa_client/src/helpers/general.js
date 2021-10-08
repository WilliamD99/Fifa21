export function getAverage(obj) {
    let avg = 0
    let length = 0
    for (let key in obj) {
        if (obj[key] !== undefined) {
            avg += obj[key]
            length += 1
        }
    }
    return avg / length
}

export function extractStar(str) {
    const arr = str.split(" ")

    return parseInt(arr[0])
}
