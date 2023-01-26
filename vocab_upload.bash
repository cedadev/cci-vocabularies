export vocab_server='vocab.ceda.ac.uk'

export html_dir='/home/mobaxterm/MyDocuments/GitHub/cci-vocabularies/html'

echo "About to copy html from ${html_dir} to ${vocab_server}"

scp -p ${html_dir}/index.html root@$vocab_server:/var/www/html/
scp -p ${html_dir}/cci.html root@$vocab_server:/var/www/html/
scp -p ${html_dir}/vocab.css root@$vocab_server:/var/www/html/
scp -p ${html_dir}/.htaccess root@$vocab_server:/var/www/html/
scp -pr ${html_dir}/error_pages root@$vocab_server:/var/www/html/

scp -pr ${html_dir}/scheme root@$vocab_server:/var/www/html/

scp -pr ${html_dir}/collection root@$vocab_server:/var/www/html/

scp -pr ${html_dir}/ontology root@$vocab_server:/var/www/html/

ssh root@$vocab_server chown -R apache:apache /var/www/html

ssh root@$vocab_server find /var/www/html -type d -exec chmod 750 {} +

ssh root@$vocab_server find /var/www/html -type f -exec chmod 640 {} +

echo
echo "FINISHED"
echo
