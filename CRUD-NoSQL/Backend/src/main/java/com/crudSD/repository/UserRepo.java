package com.crudSD.repository;

import com.crudSD.model.User;
import org.bson.types.ObjectId;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface UserRepo extends MongoRepository<User, ObjectId> {
    List<User> findByEmail(String email);
    List<User>findByName(String name);

    boolean existsByEmail(String email);

}
