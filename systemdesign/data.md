# Данные для обучения

Первичные данные берем из ответа метода
https://torgi.gov.ru/new/api/public/lotcards/{id_ad}

| Название параметра в ответе метода            | Расшифровка                                            | Тип           |
|-----------------------------------------------|--------------------------------------------------------|---------------|
| id                                            |                                                        | String        |
| lotName                                       |                                                        | String(4000)  |
| lotStatus                                     |                                                        | Enum          |
| biddForm.code                                 |                                                        |               |
| biddForm.name                                 |                                                        |               |
| noticeNumber                                  |                                                        |               |
| lotNumber                                     |                                                        |               |
| biddType.code                                 |                                                        |               |
| biddType.name                                 |                                                        |               |
| subjectRFCode                                 | Код субъекта РФ                                        | Number        |
| lotDescription                                | Описание лота                                          | String (4000) |
| priceMin                                      |                                                        | Number        |
| priceStep                                     |                                                        | Number        |
| prevBiddInfo                                  |                                                        |               |
| previousProcedures  ?                         | Массив, в примере пустой, найти и изучить не пустые!   |               |
| lotImages                                     | код в 16риной системе, как получить картинку?          |               |
| lotAttachments                                | Массив объектов типа ниже                              |               |
| lotAttachments.fileId                         |                                                        |               |
| lotAttachments.signatureId                    |                                                        |               |
| lotAttachments.fileName                       |                                                        |               |
| lotAttachments.fileSize                       |                                                        |               |
| lotAttachments.uploadDate                     |                                                        |               |
| lotAttachments.hash                           |                                                        |               |
| lotAttachments.inactive                       |                                                        |               |
| lotAttachments.checkResult                    |                                                        |
| noticeAttachments                             | Массив объектов типа ниже                              | 
| noticeAttachments.fileId                      |                                                        |               |
| noticeAttachments.signatureId                 |                                                        |               |
| noticeAttachments.fileName                    |                                                        |               |
| noticeAttachments.fileSize                    |                                                        |               |
| noticeAttachments.uploadDate                  |                                                        |               |
| noticeAttachments.hash                        |                                                        |               |
| noticeAttachments.attachmentTypeCode          |                                                        |               |
| noticeAttachments.attachmentTypeName          |                                                        |               |
| noticeAttachments.inactive                    |                                                        |               |
| noticeAttachments.checkResult                 |                                                        |
| characteristics                               |                                                        |               |
| characteristics.characteristicValue           | Строка или массив объектов                             |               |
| characteristics.characteristicValue.value     |                                                        |               |
| characteristics.characteristicValue.selectNsi |                                                        |               |
| characteristics.characteristicValue.code      |                                                        |               |
| characteristics.characteristicValue.name      |                                                        |               |
| characteristics.characteristicValue.actual    |                                                        |               |
| characteristics.name                          |                                                        |               |
| characteristics.code                          |                                                        |               |
| characteristics.unit                          | Необязательное поле                                    |               |
| characteristics.unit.code                     |                                                        |               |
| characteristics.unit.name                     |                                                        |               |
| characteristics.unit.symbol                   |                                                        |               |
| characteristics.type                          |                                                        |               |
| currencyCode                                  |                                                        |               |
| etpCode                                       |                                                        |               |
| category.code                                 |                                                        |               |
| category.name                                 |                                                        |               |
| timeZoneName                                  |                                                        |               |
| timezoneOffset                                |                                                        |               |
| ownershipForm.code                            |                                                        |               |
| ownershipForm.name                            |                                                        |               |
| etpUrl                                        |                                                        |               |
| deposit                                       |                                                        |               |
| estateAddress                                 |                                                        |               |
| attributes                                    | Массив объектов                                        |               |
| attributes.code                               |                                                        |               |
| attributes.fullName                           |                                                        |               |
| attributes.value                              | Необязательное поле  строка или объект                 |               |
| attributes.value.code                         |                                                        |               |
| attributes.value.name                         |                                                        |               |
| attributes.attributeType                      |                                                        |               |
| attributes.group                              | Объект с полями                                        |               |
| attributes.group.code                         |                                                        |               |
| attributes.group.name                         |                                                        |               |
| attributes.group.displayGroupType             |                                                        |               |
| attributes.sortOrder                          |                                                        |               |
| attributes.                                   |                                                        |               |
| depositElectronicPlatform                     |                                                        |               |
| depositRecipientName                          |                                                        |               |
| depositRecipientINN                           |                                                        |               |
| depositRecipientKPP                           |                                                        |               |
| depositBankName                               |                                                        |               |
| depositBIK                                    |                                                        |               |
| depositPayAccount                             |                                                        |               |
| depositCorAccount                             |                                                        |               |
| depositTreasuryAccount                        |                                                        |               |
| depositPurposePayment                         |                                                        |               |
| hasAppeals                                    |                                                        |               |
| isStopped                                     |                                                        |               |
| auctionStartDate                              |                                                        |               |
| biddStartTime                                 |                                                        |               |
| biddEndTime                                   |                                                        |               |
| versionId                                     |                                                        |               |
| noticeSignedData.fileId                       |                                                        |               |
| noticeSignedData.signatureId                  |                                                        |               |
| noticeSignedData.fileName                     |                                                        |               |
| noticeSignedData.fileSize                     |                                                        |               |
| noticeSignedData.uploadDate                   |                                                        |               |
| noticeSignedData.hash                         |                                                        |               |
| noticeSignedData.inactive                     |                                                        |               |
| egrkns.id                                     |                                                        |               |
| egrkns.number                                 |                                                        |               |
| egrkns.name                                   |                                                        |               |
| egrnInfoRequestList                           | Пустой массив, найти лоты с этим параметром и изучить! |               |
| noticeFirstVersionPublicationDate             |                                                        |               |
| isAnnulled                                    |                                                        | Boolean       |

Поля есть в первичном парсинге, разобраться, как 
isCompound
noticeAttributes
privatizationReason
cancellation
lotToPlanLink
protocols
cutoffPrice
priceDecreaseStep
suspensions
cutoffPrice