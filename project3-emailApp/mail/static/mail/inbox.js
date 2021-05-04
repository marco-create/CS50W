document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  // Submit the new email
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function send_email(event) {
  event.preventDefault();


  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  
  fetch('/emails', {method:'POST', body: JSON.stringify({recipients: recipients,
                                                        subject: subject,
                                                        body: body,})
  })
  .then((response) => response.json())
  .then((result) => {
    if (!recipients || !body || !subject) {
      alert('Please fill all fields!');
      compose_email;
    } else {
      load_mailbox('sent', result);
    };
  })
  .catch((error) => console.log(error));
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#load-email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  var list_recipients = [];

  document.querySelector('#users').addEventListener('click', () => {

    var x = document.getElementById('users').value;
    console.log(`Pressed: ${x}`);

    if (list_recipients.includes(x)) {
      console.log(`Do not add ${x}`);
    } else {
      list_recipients.push(x);
    }

    list_recipients.forEach(element => {
      if (element === 'Choose recipients') {
        // Remove the default selection
        list_recipients = list_recipients.filter(e => e !== element);
      }
    });

    document.querySelector('#compose-recipients').value = list_recipients;
    // list_recipients.shift();  // need to remove the first empty default value
    console.log(`List: ${list_recipients}`);
  })
  

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#load-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails)

    // Create a new "article" for each email if not archived
    emails.forEach((element) => {
      if (mailbox == 'inbox' || mailbox == 'archive') {
        if (element.read) {
          is_read = 'read';
        } else {
          is_read = '';
        }
      } else {
        is_read = '';
      };

    
      var article = document.createElement('article');
      article.className = `article ${is_read}`;
      article.innerHTML = 
      `<div class="article-wrapper">

        <h6 style="margin:0;">${element.subject}</h6>
        <p style="margin:0;">${element.body.slice(0,100)}...</p>
        <div class="article-wrap-footer">
          <span class="article-footer-span">From ${element.sender}</span>
          <span class="article-footer-span">${element.timestamp}</span>
        </div>
      </div>`;
     
      article.addEventListener('click', () => load_email(element.id))
      document.querySelector('#emails-view').appendChild(article);
    });
  });
}

function load_email(email_id, mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#load-email').style.display = 'block';
  
  // Clear the content
  document.querySelector('#load-email').innerHTML = '';

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    // Print email
    console.log(`This is the ID: ${email_id}`)
    console.log(email)

    const archive = email.archived;

    // Add div element and show the email
    var article = document.createElement('article');
    article.className = "article";

    // Create containers for storing the message
    var title = document.createElement('h5'); title.className = 'contain-subj';
    title.innerText = email.subject;
    var sender = document.createElement('h6'); sender.className = 'contain-sender';
    sender.innerText = email.sender;
    var timestamp = document.createElement('p'); timestamp.className = 'contain-time';
    timestamp.innerText = email.timestamp;
    var recipients = document.createElement('p'); recipients.className = 'contain-recipients';
    recipients.innerText = `to ${email.recipients}`;
    var body = document.createElement('p'); body.className = 'contain-body';
    body.innerText = email.body;

    // Create a div to contain sendere and time
    var info_wrapper = document.createElement('div');
    info_wrapper.className = 'info-wrapper';
    info_wrapper.appendChild(sender);
    info_wrapper.appendChild(timestamp);

    // Create buttons
    var archive_button = document.createElement('input');
    archive_button.className = 'btn archive-btn';
    archive_button.type = 'submit';
    if (!email.archived) {
      archive_button.value = 'Archive';
    } else {
      archive_button.value = 'Unarchive';
    };
    
    var reply_button = document.createElement('input');
    reply_button.className = 'btn reply-btn';
    reply_button.type = 'submit';
    reply_button.value = 'Reply';
    
    // Append all the childs to the article and to the body
    article.appendChild(title);
    article.appendChild(info_wrapper);
    article.appendChild(recipients);
    article.appendChild(body);

    document.querySelector('#load-email').appendChild(article); 
    document.querySelector('#load-email').appendChild(archive_button);
    document.querySelector('#load-email').appendChild(reply_button)
    // Switch to read
    switch_read(email_id);
    
    // Archive email
    document.querySelector('.archive-btn').addEventListener('click', () => archive_email(email_id, archive)
    );

    // Reply to email
    document.querySelector('.reply-btn').addEventListener('click', () => reply_email(email.sender, 
                                                                                    email.subject, 
                                                                                    email.timestamp, 
                                                                                    email.body));
  })
}

function switch_read(email_id) {
  // Switch to read: true when the email is selected
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
    read: true
    })
  })
}

function archive_email(email_id, archive) {
  // Come back to inbox page and move the message to archived
  load_mailbox('inbox')
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !archive
    })
  });

}

function reply_email(sender, subject, timestamp, body) {
  
  compose_email();

  const sbj = subject.includes('Re:');
  console.log(`Found "Re:"? ${sbj}.`);
  // Make some pre-populated field
  document.querySelector('#compose-recipients').value = sender;

  document.querySelector('#compose-body').value = 
  `
  ----------------------
  On ${timestamp}, ${sender} wrote: ${body}`;

  if (sbj) {
    document.querySelector('#compose-subject').value = subject;
  } else {
    document.querySelector('#compose-subject').value = `Re: ${subject}`;
  }
}