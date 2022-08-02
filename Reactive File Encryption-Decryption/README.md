# This is A Separate Repository Because It's Not Only a Telegram Bot
<a href="https://github.com/MortexAG/Reactive-File-encryption-decryption"><h1>Access It From This Link</h1></a>
# This is Tool That Can Encrypt/Decrypt Single Type of Files Or All Files in  directory.
<hr> 
<h4>Here we Will be using The "myfiles" as the directory that all the codes will run on dealing with the files inside, and add your secrets as "API_KEY" and "Chat_ID"</h4>
<hr>
<h2>
  <ul>
  <li>
  The "main.py" here controls the "encrypt_all.py" (which is explained later on) by a telegram bot, you can use the /help command to get a list of  commands.
  </li>
  </ul>
</h2>
<h3><ol>
  <li>
    First There's The "encrypt_all.py" and the "decrypt_all.py" :
    <ul>
    <h4>
     <li>
      It Converts Every File of any type that's present inside the myfiles folder to a ".mortex" file which is a simple encrypted file it can be reversed using the "decrypt()" function.  
  </li>
  <li>
    It Creats a key and stores it in the "key_all.mortkey" to be used to decrypt.
  </li>
  </h4>
  </ul>
  </li>
  <li>Then There's The "encrypt_text.py" and "decrypt_text.py" :
  <ul>
    <h4>
      <li>They Only Convert The Text Files inside the myfiles folder into encrypted files.</li>
  <li>They Generate The "key_text.mortkey" file that contains the key that will be used to decrypt the Text Files.</li>
  <li>The decrypt_text.py will return the text files to their normal state using the key.</li>
    </h4>
  </ul>
    <li>
      Then There's The "img_encrypt.py" and the "img_decrypt.py" :
  <ul>
    <h4>
  <li> 
  They Convert The Png image inside the myfiles fodler into an ecrypted image by converting it to a .mortex file then getting the text, encrypting it and returning in the file then convert it back to a Png and to decrypt it does exactly the reverse of this.        
          
  </li>
  <li>
    It creats a key and stores it inside the "key_img.mortkey" to be used to decrypt the image again.
  </li>
  </h4>
  </ul>   
</ol>
    </h3>
