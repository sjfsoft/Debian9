<?php
$channel = $_GET['channel'];
$chs = $_GET['chs'];
$url = file_get_contents('https://api.live.bilibili.com/room/v1/Room/playUrl?quality=0&platform=web&cid='.$channel);
$url = json_decode($url, true);
if ($chs="-0") {
  $url = $url['data']['durl'][0]['url'];
} elseif ($chs="-1") {
  $url = $url['data']['durl'][1]['url'];
} elseif ($chs="-2") {
  $url = $url['data']['durl'][2]['url'];
} elseif ($chs="-3") {
  $url = $url['data']['durl'][3]['url'];
}
$url = str_replace('https','http',$url);
header('location:'.$url);
exit;
?>
