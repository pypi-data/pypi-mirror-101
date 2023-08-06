
const files = require.context('./இலக்கணங்கள்/', true, /\.json$/)
const modules_takavalkal = {}
const modules_mozhippeyarpukal = {}

files.keys().forEach(key => {
  let கோப்பு = key.split('/').pop()
  if (கோப்பு === 'தகவல்கள்.json') {
    modules_takavalkal[key.replace(/(\.\/|\.json)/g, '')] = files(key).default
  } else if (கோப்பு === 'மொழிபெயர்ப்புகள்.json') {
    modules_mozhippeyarpukal[key.replace(/(\.\/|\.json)/g, '')] = files(key).default
  }
})

export const நிரல்மொழிகள் = [...new Set([].concat(...Object.keys(modules_takavalkal).map(x=>x.split('/')[0])))]

const தகவல்கள் = Object.keys(modules_takavalkal).reduce((முன், தற்) => ({ ...முன், [தற்.split('/')[0]]: require(`./இலக்கணங்கள்/${தற்}.json`) }), {})
const மொழிபெயர்ப்புகள் =  Object.keys(modules_mozhippeyarpukal).reduce((முன், தற்) => ({ ...முன், [தற்.split('/')[0]]: require(`./இலக்கணங்கள்/${தற்}.json`) }), {})

export const பதிப்பு_கண்டறி = (நிரல்மொழி) => Object.keys(தகவல்கள்[நிரல்மொழி]['பதிப்பு'] || {"":""}).slice(-1)[0]

export const விதிகள் = function (நிரல்மொழி, பதிப்பு=undefined) {
   பதிப்பு = பதிப்பு || பதிப்பு_கண்டறி(நிரல்மொழி)
   return மொழிபெயர்ப்புகள்[நிரல்மொழி]["பதிப்புகள்"][பதிப்பு]
}
export const விதி_மொழிபெயர்ப்பு = function (நிரல்மொழி, மொழி, விதி) {
   if (மொழிபெயர்ப்புகள்[நிரல்மொழி]["விதிகள்"][விதி]["தேவை"] === false) {
      return விதி
   }
   return மொழிபெயர்ப்புகள்[நிரல்மொழி]["விதிகள்"][விதி]["பெயர்ப்பு"][மொழி]
}
export const நிறைவு = function (நிரல்மொழி, மொழி, பதிப்பு=undefined) {
    if (மொழி === தகவல்கள்[நிரல்மொழி]["மொழி"]) {
        return 1
    }
    பதிப்பு = பதிப்பு || பதிப்பு_கண்டறி(நிரல்மொழி)
    let விதி_நிரல்மொழி = விதிகள்(நிரல்மொழி, பதிப்பு)
    let _விதி_மொழிபெயர்ப்பு = விதி_நிரல்மொழி.map(இ => விதி_மொழிபெயர்ப்பு(நிரல்மொழி, மொழி, இ)).filter(இ => இ)
    return _விதி_மொழிபெயர்ப்பு.length / விதி_நிரல்மொழி.length
}

export const பெயர் = (நிரல்மொழி, மொழி) => {
  return மொழிபெயர்ப்புகள்[நிரல்மொழி]["பெயர்"][மொழி]
}

export const இயற்கை_மொழிகள் = (நிரல்மொழி) => {
  let மொழிகள் = Object.values(மொழிபெயர்ப்புகள்[நிரல்மொழி]["விதிகள்"]).map(இ => Object.keys(இ["பெயர்ப்பு"])).filter(இ => இ.length)
  return [தகவல்கள்[நிரல்மொழி]["மொழி"], ...new Set([].concat(...மொழிகள்))]

}