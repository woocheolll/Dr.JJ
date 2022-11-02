const followForm = document.querySelector('.follow-form')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

followForm.addEventListener('submit', function (event) {
  event.preventDefault()
  axios({
    method: 'post',
    url: `/accounts/${followForm.dataset.userPk}/follow/`,
    headers: { 'X-CSRFToken': csrftoken },
  }).then((response) => {
    // 팔로우 버튼 토글
    const followBtn = document.querySelector('.follow-btn')
    if (response.data.is_followed === false) {
      followBtn.value = 'Follow'
    } else {
      followBtn.value = 'Unfollow'
    }

    // 팔로잉/팔로워 수 변경
    const followingCnt = document.querySelector('.following-cnt')
    const followerCnt = document.querySelector('.follower-cnt')

    followingCnt.innerText = response.data.following_cnt
    followerCnt.innerText = response.data.follower_cnt
  })
})