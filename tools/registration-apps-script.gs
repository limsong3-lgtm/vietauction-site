/**
 * VietAuction bid registrations -> Google Sheet
 *
 * Setup (5 minutes):
 * 1. Open the Google Sheet "VietAuction registrations" (My Drive > VietAuction).
 * 2. Extensions > Apps Script. Delete the sample code, paste this whole file, Save.
 * 3. Deploy > New deployment > type "Web app".
 *      Execute as: Me.   Who has access: Anyone.
 *    Click Deploy, allow the permissions, and copy the Web app URL (ends in /exec).
 * 4. In index.html set:  const REG_ENDPOINT='<that URL>';
 *    The "Preview: submissions are not collected" note disappears automatically.
 *
 * The site posts JSON as text/plain (no-cors), so this script reads e.postData.contents.
 */
const SHEET_NAME = 'Registrations';
const COLUMNS = ['at', 'auction', 'name', 'phone', 'email', 'city', 'how', 'interests', 'note'];

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const data = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sh = ss.getSheetByName(SHEET_NAME) || ss.getSheets()[0];
    if (sh.getLastRow() === 0) {
      sh.appendRow(['Received', 'Auction', 'Name', 'Phone / Zalo', 'Email', 'City', 'How to bid', 'Interested in', 'Note']);
      sh.setFrozenRows(1);
    }
    // Strip leading = + - @ so a submitted value can never run as a formula in the sheet.
    const clean = v => String(v == null ? '' : v).slice(0, 1000).replace(/^[=+\-@]+/, "'$&");
    sh.appendRow(COLUMNS.map(k => k === 'at' ? new Date() : clean(data[k])));
    return ContentService.createTextOutput('ok');
  } finally {
    lock.releaseLock();
  }
}
