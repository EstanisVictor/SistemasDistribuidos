package CRUDSD.Controller;

import CRUDSD.Model.User;
import CRUDSD.Service.UserService;
import org.bson.types.ObjectId;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@CrossOrigin
@RestController
@RequestMapping(value="/")
public class UserController {
    private final String EMAIL_REGEX = "^[A-Za-z0-9+_.-]+@(.+)$";
    private final Pattern pattern = Pattern.compile(EMAIL_REGEX);
    private final UserService userService;
    @Autowired
    public UserController(UserService userService) {
        this.userService = userService;
    }

    public boolean isEmailValid(String email){
        Matcher matcher = pattern.matcher(email);
        return matcher.matches();
    }

    @PostMapping("/register")
    public CustomResponse saveUser(@RequestBody User user){

        CustomResponse response = new CustomResponse();

        if(userService.existsByEmail(user.getEmail())){
            response.setStatus(HttpStatus.CONFLICT.value());
            response.setMessage("User with email {" + user.getEmail() + "} already exists");
        }else if (!isEmailValid(user.getEmail())){
            response.setStatus(HttpStatus.BAD_REQUEST.value());
            response.setMessage("Email {" + user.getEmail() + "} is not valid");
        }else{
            response.setStatus(HttpStatus.CREATED.value());
            response.setData(userService.generateUser(user));
        }

        return response;
    }

    @GetMapping("/getAll")
    public List<User> getAllUsers(){
        return userService.findAllUsers();
    }

    @GetMapping("/getUser/{id}")
    public CustomResponse getUserById(@PathVariable(value="id") String id){
        CustomResponse response = new CustomResponse();
        Optional<User> user = userService.findUserById(id);

        if(!user.isPresent()){
            response.setStatus(HttpStatus.NOT_FOUND.value());
            response.setMessage("User with id " + id + " not found");
        } else {
            response.setStatus(HttpStatus.OK.value());
            response.setData(user.get());
        }

        return response;
    }

    @GetMapping("/getEmail/{email}")
    public CustomResponse getUserByEmail(@PathVariable String email){
        CustomResponse response = new CustomResponse();
        List<User> user = userService.findUserByEmail(email);

        if(user.isEmpty()){
            response.setStatus(HttpStatus.NOT_FOUND.value());
            response.setMessage("User with email {" + email + "} not found");
        } else {
            response.setStatus(HttpStatus.OK.value());
            response.setData(user);
        }

        return response;
    }

    @GetMapping("/getName/{name}")
    public CustomResponse getUserByName(@PathVariable String name){
        CustomResponse response = new CustomResponse();
        List<User> user = userService.findUserByName(name);

        if(user.isEmpty()){
            response.setStatus(HttpStatus.NOT_FOUND.value());
            response.setMessage("User with name {" + name + "} not found");
        } else {
            response.setStatus(HttpStatus.OK.value());
            response.setData(user);
        }

        return response;
    }

    @DeleteMapping("/delete/{id}")
    public CustomResponse deleteUser(@PathVariable(value="id") String id){
        CustomResponse response = new CustomResponse();
        Optional<User> user = userService.findUserById(id);

        if(!user.isPresent()){
            response.setStatus(HttpStatus.NOT_FOUND.value());
            response.setMessage("User with id {" + id + "} not found");
        } else {
            userService.deleteUser(user.get());
            response.setStatus(HttpStatus.OK.value());
            response.setMessage("User with id {" + id + "} deleted successfully");
        }

        return response;
    }

    @PutMapping("/users/{id}")
    public Object updateUser(@PathVariable String id, @RequestBody User novoUser){
        CustomResponse response = new CustomResponse();
        Optional<User> userOptional = userService.findUserById(id);

        if(!userOptional.isPresent()){
            response.setStatus(HttpStatus.NOT_FOUND.value());
            response.setMessage("User with id {" + id + "} not found");
        } else if (novoUser.getEmail() == null || novoUser.getName() == null){
            response.setStatus(HttpStatus.BAD_REQUEST.value());
            response.setMessage("User with id {" + id + "} not updated, because the new data is null");
        } else {
            User existingUser = userOptional.get();
            existingUser.setEmail(novoUser.getEmail());
            existingUser.setName(novoUser.getName());
            userService.generateUser(existingUser);

            response.setStatus(HttpStatus.OK.value());
            response.setMessage("User with id {" + id + "} updated successfully with new data {" + novoUser.getName() + "} and {" + novoUser.getEmail() + "}");
        }

        return response.data;
    }

    public static class CustomResponse {
        private int status;
        private String message;
        private Object data;

        public int getStatus() {
            return status;
        }

        public void setStatus(int status) {
            this.status = status;
        }

        public String getMessage() {
            return message;
        }

        public void setMessage(String message) {
            this.message = message;
        }

        public Object getData() {
            return data;
        }

        public void setData(Object data) {
            this.data = data;
        }
    }
}
