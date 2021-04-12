export const average = (data: number[]): number => {
    return data.reduce((a, b) => 
        a + b, 0) / data.length;
};

// Calculate standard error of the mean. Used to plot
// confidence intervals. 
export const standardError = (data: number[]): number => {
    return Math.sqrt(data.reduce((a, b) => 
        a + Math.pow(b - average(data), 2), 0) / 
        (data.length - 1) / data.length);
};

// Sort the data in descending order, and return
// the middle element. The input array is expected
// to have an even number of elements, so return
// the element at index (length / 2 - 1). 
export const median = (data: number[]): number => {
    const sortedData = [...data].sort((a, b) => b - a);
    return sortedData[Math.floor(sortedData.length / 2) - 1];
};