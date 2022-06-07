<script setup lang="ts">
import {ref, reactive} from 'vue'
import axios from 'axios'

// 型を定義する場合は冒頭に type を使う (interface を使った書き方もある。その場合は "=" を外す)
type typeOfFeatures = {
  Sex: '男性'|'女性'|'性別は？'
  Pclass: string
  Age: number|'年齢は？'
  Parch: number|'親・子の同伴者数は？'
  SibSp: number|'兄弟姉妹の同伴者数は？'
}

const features = reactive<typeOfFeatures>({
  Sex: '性別は？',
  Pclass: '階級は？',
  Age: '年齢は？',
  Parch: '親・子の同伴者数は？',
  SibSp: '兄弟姉妹の同伴者数は？'
})

// const displayOutput = (): void => {
//   alert(`
//     性別: ${features.Sex}
//     階級: ${features.Pclass} 
//     年齢: ${features.Age} 
//     親・子同伴者数: ${features.Parch} 
//     兄弟姉妹同伴者数: ${features.SibSp}
//   `)
// }

// 生存確率を格納するための箱を作る
const survivalProbability = ref<number|undefined>()
// バリデーションのための関数を定義。
const validateRequestValues = (): boolean => {
  if (features.Sex == '性別は？') {
    alert('性別を入力してください。')
    return false
  }
  if (features.Pclass == '階級は？') {
    alert('階級を入力してください。')
    return false
  } 
  if (features.Age == '年齢は？') {
    alert('年齢を入力してください。')
    return false
  } 
  if (features.Parch == '親・子の同伴者数は？') {
    alert('親子同伴者数を入力してください。')
    return false
  } 
  if (features.Pclass == '兄弟姉妹の同伴者数は？') {
    alert('兄弟姉妹同伴者数を入力してください。')
    return false
  }
  // 全ての条件に引っかからなかった場合にのみ true を返す
  return true
  
}

const displayOutput = (): void => {
  // エンドポイントを指定
  const endPoint: string = 'http://localhost:5000/api/titanic'
  // バリデーションの実行
  const validationResult: boolean = validateRequestValues()
  // バリデーションに成功していれば axios を実行
  if (validationResult === true) {  
    // axios.post で POST メソッドを実行することを指示。
    // 第一引数にエンドポイント, 第二引数にリクエストボディを指定。
    axios.post(
      endPoint, features
    ).then(
      // then 以下で問題なくレスポンスが返ってきた際の挙動を記述
      (response) => {
        // TypeScriptの型指定は後ろに as をこのように付けることでも可能。
        survivalProbability.value = 100 * response.data.survival_probability as number
      }
    ).catch(
      // catch 以下では問題があった際の挙動を記述
      () => {
        alert('エラーが発生しました。')
      } 
    )
  }
}

</script>

<template>
<p class="bg-blue-200 text-2xl p-4">Hello World!</p>
<div class="container mx-auto mt-4">
  <select class="select select-primary mb-4" v-model="features.Sex">
    <option disabled selected>性別は？</option>
    <option>男性</option>
    <option>女性</option>
  </select>
  <br>
  <select class="select select-primary mb-4" v-model="features.Pclass">
    <option disabled selected>階級は？</option>
    <option>上層クラス（お金持ち）</option>
    <option>中級クラス（一般階級）</option>
    <option>下層クラス（労働階級）</option>
  </select>
  <br>
  <select class="select select-primary mb-4" v-model="features.Age">
    <option disabled selected>年齢は？</option>
    <option v-for="i in [...Array(121).keys()]">
      {{ i }} 
    </option>
  </select> 歳
  <br>
  <select class="select select-primary mb-4" v-model="features.Parch">
    <option disabled selected>親・子の同伴者数は？</option>
    <option v-for="i in [...Array(11).keys()]">
      {{ i }} 
    </option>
  </select> 人
  <br>
  <select class="select select-primary mb-4" v-model="features.SibSp">
    <option disabled selected>兄弟姉妹の同伴者数は？</option>
    <option v-for="i in [...Array(11).keys()]">
      {{ i }}
    </option>
  </select> 人
  <br>
  <button class="btn btn-primary" v-on:click="displayOutput()">結果を出力</button>
  <template v-if="survivalProbability !== undefined">
    <div class="alert alert-error mt-4 ">
      あなたの生存確率は {{ Math.round(survivalProbability) }} % です。
    </div>
  </template>
</div>
</template>
