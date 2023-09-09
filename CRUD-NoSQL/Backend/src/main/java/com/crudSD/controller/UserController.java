package com.crudSD.controller;

import com.crudSD.model.User;
import com.crudSD.service.UserService;
import org.bson.types.ObjectId;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
@CrossOrigin(origins = "*")
@RestController
@RequestMapping(value="/api")
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

    @PostMapping("/generate")
    public ResponseEntity<Object> saveUser(@RequestBody User user){

        if(userService.existsByEmail(user.getEmail())){
            return ResponseEntity.status(HttpStatus.CONFLICT).body("User with email {" + user.getEmail() + "} already exists");
        }

        if (!isEmailValid(user.getEmail())){
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Email {" + user.getEmail() + "} is not valid");
        }

        return ResponseEntity.status(HttpStatus.CREATED).body(userService.generateUser(user));
    }

    @GetMapping("/getAll")
    public List<User> getAllUsers(){
        return userService.findAllUsers();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Object> getUserById(@PathVariable(value="id") ObjectId id){

        Optional<User> user = userService.findUserById(id);

        if(!user.isPresent()){
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("User with id " + id + " not found");
        }

        return ResponseEntity.status(HttpStatus.OK).body(user.get());
    }

    @GetMapping("/getEmail/{email}")
    public ResponseEntity<Object> getUserByEmail(@PathVariable String email){

        List<User> user = userService.findUserByEmail(email);

        if(user.isEmpty()){
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("User with email {" + email + "} not found");
        }

        return ResponseEntity.status(HttpStatus.OK).body(user);
    }

    @GetMapping("/getName/{name}")
    public ResponseEntity<Object> getUserByName(@PathVariable String name){

        List<User> user = userService.findUserByName(name);

        if(user.isEmpty()){
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("User with name {" + name + "} not found");
        }

        return ResponseEntity.status(HttpStatus.OK).body(user);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Object> deleteUser(@PathVariable(value="id") ObjectId id){

        Optional<User> user = userService.findUserById(id);

        if(!user.isPresent()){
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("User with id {" + id + "} not found");
        }

        userService.deleteUser(user.get());

        return ResponseEntity.status(HttpStatus.OK).body("User with id {" + id + "} deleted successfully");
    }

    @PutMapping("/{id}")
    public ResponseEntity<Object> updateUser(@PathVariable ObjectId id, @RequestBody User novoUser){

        Optional<User> userOptional = userService.findUserById(id);

        if(!userOptional.isPresent()){
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("User with id {" + id + "} not found");
        }

        if(novoUser.getEmail() == null || novoUser.getName() == null){
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("User with id {" + id + "} not updated, because the new data is null");
        }

        userOptional.get().setEmail(novoUser.getEmail());
        userOptional.get().setName(novoUser.getName());

        userService.generateUser(userOptional.get());

        return ResponseEntity.status(HttpStatus.OK).body("User with id {" + id + "} updated successfully with new data {" + novoUser.getName() + "} and {" + novoUser.getEmail() + "}");
    }
}
