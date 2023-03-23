document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => {load_mailbox('inbox')});
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);


  
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-open').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  const recipients = document.querySelector('#compose-recipients');
  const subject = document.querySelector('#compose-subject');
  const body = document.querySelector('#compose-body');

  recipients.value = '';
  subject.value = '';
  body.value = '';

  const composeForm = document.querySelector('#compose-form');
  
  composeForm.addEventListener('submit', (event) => {
    event.preventDefault();
    send(recipients.value, subject.value, body.value);
  })

}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-open').style.display = 'none';
  
  const mailContainer = document.querySelector('#emails-view');

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;


  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      emails.forEach(email => {
        
        const emailBox = document.createElement('article');
        emailBox.classList.add('email');
        
        const sender = document.createElement('p');
        sender.classList.add('email__sender')
        sender.innerHTML = email.sender;

        const subject = document.createElement('h4');
        subject.classList.add('email__subject');
        subject.innerHTML = email.subject;

        const timestamp = document.createElement('time');
        timestamp.classList.add('email__timestamp');
        timestamp.innerHTML = email.timestamp;

        if (email.read === true) {
          emailBox.classList.add('email--read')
        }

        emailBox.append(sender, subject, timestamp);

        emailBox.addEventListener('click', () => {
          mark_read(email.id);         
        });

        mailContainer.append(emailBox);
      })
  }) 
}

function view_email(id) {
  document.querySelector('#email-open').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';

  const emailContainer = document.querySelector('#email-open');

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    const emailBox = document.createElement('article');

    const archiveButton = document.createElement('button');
    const replyButton = document.createElement('button');
    
    replyButton.classList.add('btn', 'btn-sm', 'btn-outline-primary');
    replyButton.innerHTML = 'Reply';

    replyButton.addEventListener('click', () => {
      reply(email.sender, email.subject, email.timestamp, email.body);
    })

    archiveButton.classList.add('btn', 'btn-sm', 'btn-outline-primary');
    
    if (email.archived) {
      archiveButton.innerHTML = 'Unarchive';
    }
    else {
      archiveButton.innerHTML = 'Archive';
    }
    
    archiveButton.addEventListener('click', () => {
      archive(email.id, email.archived);
    })


    const heading = document.createElement('h3');
    heading.classList.add('email-open__heading');
    heading.innerHTML = email.subject;

    const info = document.createElement('div');
    info.classList.add('email-open__info');

    const sender = document.createElement('p');
    sender.classList.add('email-open__sender');
    sender.innerHTML = `from: ${email.sender}`;

    const recipients = document.createElement('p');
    recipients.innerHTML = 'To: ';
    email.recipients.forEach((recipient, idx) => {
      recipients.innerHTML += recipient;
      if (idx != email.recipients.length - 1) {recipients.innerHTML += ', '};
    })

    const timestamp = document.createElement('p');
    timestamp.classList.add('email-open__timestamp');
    timestamp.innerHTML = email.timestamp;

    info.append(sender, timestamp);

    const body = document.createElement('p');
    body.classList.add('email-open__body');
    body.innerHTML = email.body;

    emailBox.append(heading, info, recipients, body, replyButton, archiveButton);

    emailContainer.replaceChildren(emailBox);

  })
}

function mark_read(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
  .finally(() => {
    view_email(id);
  })  
}


function send(recipients, subject, body) {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .finally(() => {
    load_mailbox('sent');
  })
}


function reply(recipient, subject, timestamp, body) {

  compose_email();
  document.querySelector('#compose-recipients').value = recipient;
  if (!subject.startsWith('RE: ')) {
    document.querySelector('#compose-subject').value += 'RE: ';
  }
  document.querySelector('#compose-subject').value += subject;
  document.querySelector('#compose-body').value = `On ${timestamp} ${recipient} wrote:\n${body}\n------------\n`;

}

function archive(id, archived) {

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: !archived
    })
  })
  .finally(() => {
    load_mailbox('inbox');
  })
} 
