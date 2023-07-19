<?php
$text = $_GET['text'];
function ConvertText($text){
    if(isset($text)) {
    $post = [
'TranslitForm[original_text]' => $text
    ];
    $ch = curl_init('https://kiril-lotin.uz/');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $post);
    $response = curl_exec($ch);
    $ex = explode('TranslitForm_convert_text">',$response);
        return explode('</textarea>',$ex[1])[0];
    }else{
        return json_encode(['msg' => 'error']);
    }
}

echo ConvertText($text);