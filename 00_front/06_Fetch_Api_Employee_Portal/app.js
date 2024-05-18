import { BrainHttp } from "./api/BrainHttp.js";

const serverURL2 = `http://127.0.0.1:5000`
// content loaded
window.addEventListener('DOMContentLoaded', function(){
    fetchEmployees()
})

let fetchEmployees = () => {
    let url = `${serverURL2}/employees`
    BrainHttp.get(url).then( (data ) => {
        let employees = data
        console.log(employees)
        let rows = ''
        for (let employee of employees) {
            rows += `<tr>
                        <td>${employee.id}</td>
                        <td>${employee.name}</td>
                        <td>${employee.email}</td>
                        <td>${employee.age}</td>
                        <td>
                            <button class="update-button" id="update">UPDATE</button>
                            <button class="delete-button" id="delete">DELETE</button>
                        </td>
                    </tr>`
        }
        document.querySelector('#table-body').innerHTML = rows
    }).catch( (err) => {
        console.log(err)
    })
}

//Add form
let employeeForm = document.querySelector('#form-post')
employeeForm.addEventListener('submit', function(e) {
    e.preventDefault()

    let employee = {
        name: document.querySelector('#add-name').value,
        email: document.querySelector('#add-email').value,
        age: document.querySelector('#add-age').value

    };

    let url = `${serverURL2}/employees`;
    BrainHttp.post(url, employee).then( (data )=>{
        console.log(data)
        fetchEmployees()
        clearFormFields()
    }).catch( (err) => {
        console.log(err)
    })

    let clearFormFields = () => {
        document.querySelector('#add-name').value = "";
        document.querySelector('#add-email').value = "";
        document.querySelector('#add-age').value = "";

    }
})


//finding selected id after clicking on an element(update or delete button) on the table
let entireTable = document.querySelector('#table-body')
entireTable.addEventListener('click', function(e){
    let targetElement = e.target
    //console.log(targetElement)

    //click delete button
    if (targetElement.classList.contains('delete-button')){
        //console.log('you have clicked delete')
       let  empId = targetElement.parentElement.parentElement.firstElementChild.innerHTML
       //console.log(empId)
       let url = `${serverURL2}/employees/${empId}`
       BrainHttp.delete(url).then( (data) => {
        console.log(data)
        fetchEmployees()

       }).catch( (err) => {
        console.log(err)
       } )

       
    }

    
     //click update  button
     if (targetElement.classList.contains('update-button')){
        //console.log('you have clicked delete')
       let  empId = targetElement.parentElement.parentElement.firstElementChild.innerHTML
       
        let url = `${serverURL}/employees`
        BrainHttp.get(url).then( (data ) => {
        let employees = data
        let selectedEmployee = employees.find((employee) => {
            return employee.id === empId

        })
        console.log(selectedEmployee)
    }).catch( (err) => {
        console.log(err)
    })
      
    }
})