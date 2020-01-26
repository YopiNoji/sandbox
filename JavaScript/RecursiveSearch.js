// 入れ子構造になったオブジェクトで再帰的にchildrenを探索
function RecursiveSearch(theObject) {
    var result = [];
    if(theObject instanceof Array) {
        for(var i = 0; i < theObject.length; i++) {
            result = RecursiveSearch(theObject[i]);
            if (result) {
                break;
            }   
        }
    }
    else
    {
        for(var prop in theObject) {
            console.log(prop + ': ' + theObject[prop]);
            if(prop == 'search_key'){
                console.log(prop + ': ' + theObject[prop]);
                result.unshift(theObject[prop]);
            }
            if(prop == 'id') {
                if(theObject[prop] == "children") {
                    return theObject;
                }
            }
            if(theObject[prop] instanceof Object || theObject[prop] instanceof Array) {
                result = RecursiveSearch(theObject[prop]);
                if (result) {
                    break;
                }
            } 
        }
    }
    return result;
}