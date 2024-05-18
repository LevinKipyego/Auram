export class BrainHttp{
    constructor (){

    }

    //GET request
     static get(url) {
        return new Promise((resolve, reject) => {
            fetch(url)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    resolve(data);
                    //let employees = data
                    //console.log(employees)
                })
                .catch(error => {
                    console.error('Error:', error);
                    reject(error);
                });
        });
    }
    

    //POST REQUEST
    static post(url,data){
        return new Promise ( ( resolve, reject ) => {
            fetch(url, {
                mode:'no-cors',
                method:'POST',
                headers:{
                    'Content-Type':'application/json'
                },
                body:JSON.stringify(data)
            }).then( (response) => {
                if (!response.ok){
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json()
            }).then( ( data ) => {
                resolve(data)
            }).catch(( err ) => {
                reject(err)
            })
        })
    }

    //PuT REQUEST
    static put(url,data){
        return new promise ( ( resolve, reject ) => {
            fetch(url, {
                method:'PUT',
                headers:{
                    'Content-Type':'application/json'
                },
                body:JSON.stringify(data)
            }).then( (response) => {
                response.json().then( (data) => {
                    resolve(data)
                }).catch( ( err ) => {
                    reject(err)
                })
            })
        })
    }

    //DELETE REQUEST
    static delete(url,data){
        return new Promise ( ( resolve, reject ) => {
            fetch(url, {
                method:'DELETE',
                headers:{
                    'Content-Type':'application/json'
                }
                
            }).then( (response) => {
                if (!response.ok){
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json()
            }).then( ( data ) => {
                resolve(data)
            }).catch(( err ) => {
                reject(err)
            })
        })
    }
}

