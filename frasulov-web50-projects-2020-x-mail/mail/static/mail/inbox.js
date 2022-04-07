document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
  document.querySelector('form').onsubmit = () =>
  {
    subj = document.getElementById('compose-subject').value
    body = document.getElementById('compose-body').value;
    recipients = document.getElementById('compose-recipients').value
    compose(recipients,subj, body)
    window.scrollTo(0, 0);
    document.getElementById('compose-subject').value = ""
    document.getElementById('compose-body').value = "";
    document.getElementById('compose-recipients').value ="";
    return false;
  }
});

function inbox(location)
{
    fetch(`/emails/${location}`)
    .then(response => response.json())
    .then(emails => {
        emails.forEach(function(email){
            email_view(email, location)
        })
    });
}

function compose(recipients,subject, body){
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      if (result.error){
          message = document.querySelector('.bg-danger');
          message.innerHTML = result.error;
          message.classList.remove('d-none')
          message.classList.add('d-block')
          setTimeout(function(){
          message.style.animationPlayState = 'running'
          message.addEventListener('animationend', () => {
          message.style.animationPlayState = 'paused'
          message.classList.remove('d-block');
          message.classList.add('d-none');
          })
      }, 6000)
        }
      else{
        load_mailbox('sent')
      }
      
        });
}

function email_view(email, location){
    const maindiv = document.createElement('div');
    maindiv.classList.add('email')
    if (email.read === false)
      maindiv.style.background = 'white'
    else
      maindiv.style.background = 'rgba(0,0,0,0.1)'

    const sender_text = document.createElement('h4');
    sender_text.innerHTML = email.sender;
    sender_text.classList.add('sender')
    const subj = document.createElement('p')
    subj.innerHTML = email.subject;
    subj.classList.add('subject')
    const date = document.createElement('p')
    date.innerHTML = email.timestamp;
    date.classList.add('date')
    maindiv.append(sender_text)
    maindiv.append(subj)
    maindiv.append(date)
    document.querySelector('#emails-view').append(maindiv)
    maindiv.onclick = () => {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })

      })
      .then( () => {
        open_mail(email, location)
      })      
    }
}

function open_mail(mail, location){
  fetch(`/emails/${mail.id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);
  

      // ... do something else with email ...
      single_mail_view(email, location)


  });

}

function single_mail_view(email, location)
{
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#info-mail').style.display = 'block';
  document.querySelector('#info-mail').innerHTML = "";
  const maindiv = document.createElement('div')
  maindiv.classList.add('mail_info')


  // from
  const from = document.createElement('div')
  let const_var = document.createElement('span')
  const_var.classList.add('static')
  const_var.innerHTML = "From:"
  const from_span = document.createElement('span')
  from_span.innerHTML = email.sender;
  from.append(const_var)
  from.append(from_span);
  // to
  const to = document.createElement('div')
  const_var = document.createElement('span')
  const_var.classList.add('static')
  const_var.innerHTML = "To:"
  const to_span = document.createElement('span')
  to_span.innerHTML = email.recipients
  to.append(const_var)
  to.append(to_span);
  
  //subject
  const subj = document.createElement('div')
  const_var = document.createElement('span')
  const_var.classList.add('static')
  const_var.innerHTML = "Subject:"
  const subj_span = document.createElement('span')
  subj_span.innerHTML = email.subject;
  subj.append(const_var)
  subj.append(subj_span);

  // timestamp

  const time = document.createElement('div')
  const_var = document.createElement('span')
  const_var.classList.add('static')
  const_var.innerHTML = "Timestamp:"
  const time_span = document.createElement('span')
  time_span.innerHTML = email.timestamp;
  time.append(const_var);
  time.append(time_span);
  
  // reply button

  const button = document.createElement('button')
  button.classList.add('btn');
  button.classList.add('btn-outline-primary')
  button.innerHTML = "Reply"
  button.onclick = () => {
    reply(email)
  }


  const text = document.createElement('p')
  let body_text_2 = email.body;
  body_text_2 = body_text_2.replace(/\n/g, "<br />");
  text.innerHTML = body_text_2;

  maindiv.append(from);
  maindiv.append(to);
  maindiv.append(subj);
  maindiv.append(time);
  maindiv.append(button);
  if (location === 'inbox')
  {
    const archive = document.createElement('button')
    archive.classList.add('btn');
    archive.classList.add('btn-outline-primary')
    archive.innerHTML = "Archive"
    archive.style.marginLeft = '5px'
    archive.onclick = () => {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true
        })
      })
      .then( () => {
        load_mailbox('inbox')
      })
    }
    maindiv.append(archive)
  } else if(location === 'archive'){
    const archive = document.createElement('button')
    archive.classList.add('btn');
    archive.classList.add('btn-outline-primary')
    archive.style.marginLeft = '5px'
    archive.innerHTML = "Unarchive"
    archive.onclick = () => {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: false
        })
      })
      .then( () => {
        load_mailbox('inbox')
      })
    }
    maindiv.append(archive)
  }
  maindiv.append(document.createElement('hr'))
  maindiv.append(text)
  document.querySelector('#info-mail').append(maindiv);
}

function reply(email) {
  console.log(email)
  compose_email()
  document.querySelector('#compose-recipients').value = email.sender;
  if (email.subject.substring(0, 3) !== 'Re:')
    document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
  else
    document.querySelector('#compose-subject').value = email.subject;
  let body_text = `${email.timestamp} ${email.sender} wrote:\n${email.body}\n---------------------------------------------------------------------\n`
  document.querySelector('#compose-body').value = body_text;
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#info-mail').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#info-mail').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  if (mailbox === 'inbox'){
    inbox('inbox')
  }else if(mailbox === 'sent'){
    inbox('sent')
  }else if (mailbox === 'archive'){
    inbox('archive')
  }
}