<?php
 require_once('db.php');
class Utilisateur
{
    public function create($nom,$prenom,$tel,$email,$password)
    {
        $hashedPassword = password_hash($password,PASSWORD_BCRYPT);
        //insertion des donnees//
        $rep=$db->prepare('INSERT INTO huser(nom,prenom,tel,email,password) value(:nom,:prenom,:tel,:email,:passwds)');
        $nom=$rep->execute(array(
            'nom'=>$nom;
            'prenom'=>$prenom;
            'tel'=>$tel;
            'email'=>$email;
            'passwds'=>$hashedPassword 
        ));
        //verfication des données//
        if($rep){
            $vrai=1;
            return $vrai:
        }
        else{
            $vrai=0;
            return $vrai
        }
    }
}
?>