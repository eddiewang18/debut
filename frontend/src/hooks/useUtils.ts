export default function () {
    function isInteger(test_str:string) {
        if (isNaN(parseInt(test_str))) {
            return false
        }
        if ((test_str+"").includes(".")) { 
            return false 
        }
        return true && test_str
    }

    return [isInteger]
}