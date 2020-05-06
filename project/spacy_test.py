import spacy

nlp = spacy.load('en_core_web_sm')

test_data = ("Massachusetts Financial Services Co. MA trimmed its holdings in shares of DXC Technology Co (NYSE:DXC) by 96.3% in the 4th quarter, according to the company in its most recent disclosure with the Securities & Exchange Commission. The firm owned 180,632 shares of the company’s stock after selling 4,761,209 shares during the period. Massachusetts Financial Services Co. MA owned about 0.07% of DXC Technology worth $6,790,000 at the end of the most recent reporting period.\nA number of other hedge funds and other institutional investors have also bought and sold shares of the business. FUKOKU MUTUAL LIFE INSURANCE Co boosted its position in DXC Technology by 19.8% during the fourth quarter. FUKOKU MUTUAL LIFE INSURANCE Co now owns 2,421 shares of the company’s stock valued at $91,000 after buying an additional 400 shares during the period. DNB Asset Management AS boosted its position in DXC Technology by 0.5% during the fourth quarter. DNB Asset Management AS now owns 94,730 shares of the company’s stock valued at $3,561,000 after buying an additional 430 shares during the period. Moors & Cabot Inc. boosted its position in DXC Technology by 5.7% during the fourth quarter. Moors & Cabot Inc. now owns 8,088 shares of the company’s stock valued at $306,000 after buying an additional 433 shares during the period. Franklin Resources Inc. boosted its position in DXC Technology by 4.3% during the fourth quarter. Franklin Resources Inc. now owns 10,972 shares of the company’s stock valued at $413,000 after buying an additional 455 shares during the period. Finally, Duncker Streett & Co. Inc. bought a new position in shares of DXC Technology during the fourth quarter valued at about $27,000. Institutional investors and hedge funds own 91.78% of the company’s stock. Get DXC Technology alerts:\nShares of NYSE DXC opened at $11.67 on Friday. DXC Technology Co has a fifty-two week low of $7.90 and a fifty-two week high of $67.09. The company has a 50 day simple moving average of $24.76 and a two-hundred day simple moving average of $31.12. The company has a market capitalization of $3.16 billion, a price-to-earnings ratio of 1.90, a P/E/G ratio of 0.82 and a beta of 2.10. The company has a debt-to-equity ratio of 0.80, a quick ratio of 0.93 and a current ratio of 0.93.\nDXC Technology (NYSE:DXC) last posted its quarterly earnings results on Thursday, February 6th. The company reported $1.25 EPS for the quarter, beating the Zacks’ consensus estimate of $1.08 by $0.17. DXC Technology had a negative net margin of 7.98% and a positive return on equity of 16.98%. The firm had revenue of $5.02 billion for the quarter, compared to analysts’ expectations of $4.90 billion. During the same quarter in the prior year, the company posted $2.23 earnings per share. The business’s revenue for the quarter was down 3.0% on a year-over-year basis. On average, analysts forecast that DXC Technology Co will post 5.39 earnings per share for the current fiscal year.\nThe company also recently declared a quarterly dividend, which will be paid on Tuesday, April 14th. Stockholders of record on Wednesday, March 25th will be issued a dividend of $0.21 per share. This represents a $0.84 dividend on an annualized basis and a dividend yield of 7.20%. The ex-dividend date of this dividend is Tuesday, March 24th. DXC Technology’s payout ratio is 10.07%.\nSeveral equities analysts have recently commented on DXC shares. Morgan Stanley reaffirmed a “buy” rating and set a $35.00 price objective on shares of DXC Technology in a research note on Wednesday, March 11th. BMO Capital Markets upped their price objective on shares of DXC Technology to $43.00 in a research note on Friday, December 20th. Moffett Nathanson raised shares of DXC Technology from a “neutral” rating to a “buy” rating and set a $30.00 price objective for the company in a research note on Thursday, March 12th. Citigroup upped their price objective on shares of DXC Technology from $40.00 to $41.00 and gave the company a “buy” rating in a research note on Wednesday, January 15th. Finally, Wells Fargo & Co lowered their price objective on shares of DXC Technology from $36.00 to $18.00 and set an “underweight” rating for the company in a research note on Wednesday, March 11th. Three investment analysts have rated the stock with a sell rating, six have assigned a hold rating and nine have given a buy rating to the company. DXC Technology currently has an average rating of “Hold” and an average target price of $45.86.\nAbout DXC Technology\nDXC Technology Company, together with its subsidiaries, provides information technology services and solutions primarily in North America, Europe, Asia, and Australia. It operates through three segments: Global Business Services (GBS), Global Infrastructure Services (GIS), and United States Public Sector (USPS).\nFeatured Article: FAANG Stocks Receive News & Ratings for DXC Technology analysts' ratings for DXC Technology and related companies daily email newsletter .")

doc = nlp(test_data)

ents = [(x.text, x.label_) for x in doc.ents]



for x in range(len(ents)):
    if ents[x][1] == 'LOC':
        print(ents[x])
    if ents[x][1] == 'ORG':
        print(ents[x])
    if ents[x][1] == 'DATE':
        print(ents[x])
    if ents[x][1] == 'MONEY':
        print(ents[x])
    if ents[x][1] == 'PERCENT':
        print(ents[x])
    if ents[x][1] == 'CARDINAL':
        print(ents[x])
    if ents[x][1] == 'GPE':
         print(ents[x])
    if ents[x][1] == 'PERSON':
        print(ents[x])
    

