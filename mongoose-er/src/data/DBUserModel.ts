import { Model, model, Schema } from '@hokify/db-connection';
import type {
	CVColor,
	CVFont,
	EducationStatus,
	Gender,
	ICompany,
	ICountry,
	ICvSkill,
	IEducationDegree,
	IEducationLevel,
	IJobField,
	IRecruiterProfile,
	IReferencePosition,
	IReferenceRelation,
	ISchool,
	IUser,
	IUserCvEducation,
	IUserCvExperience,
	IUserCvReference,
	IUserCvSkill,
	IUserExtra,
	IUserExtraAntiVirusResult,
	IUserInternal,
	IUserJobFilter,
	TesterGroup,
	TypeObjectId,
	UserExtraType,
	IUserGeneralAddress,
	CVLineSpacing
} from '@hokify/common';
import { AVAILABLE_CV_COLORS, AVAILABLE_CV_LINESPACINGS } from '@hokify/common';

export interface IDBUserCvEducation {
	_id: TypeObjectId<IUserCvEducation>;
	_school?: TypeObjectId<ISchool>;
	_level?: TypeObjectId<IEducationLevel>;
	_sublevel?: TypeObjectId<IEducationLevel>;
	_degree?: TypeObjectId<IEducationDegree>;
	// alternative: string; // @deprecated (if school is empty?)
	description?: string;
	startDate?: Date;
	endDate?: Date;
	// isVisible: boolean;
	status?: EducationStatus;
}

export interface IDBUserCvExperience {
	_id: TypeObjectId<IUserCvExperience>;
	title?: string;
	summary?: string;
	company?: {
		name: string;
		_relatedCompany?: TypeObjectId<ICompany>;
	};
	_fields?: TypeObjectId<IJobField>[]; // [{ type: Schema.Types.ObjectId, ref: 'Jobfield' }];f
	startDate?: Date;
	endDate?: Date;
	isCurrent?: boolean;
	// isProfession?: boolean; // @deprecated
	// isVisible: boolean;
}

export interface IDBUserCvSkill {
	_id: TypeObjectId<IUserCvSkill>;
	_category?: TypeObjectId<ICvSkill>; // type: Schema.Types.ObjectId, ref: 'CVSkill' };
	title?: string;
	text?: string;
	order?: number;
	items?: {
		name: string;
		level?: number;
	}[];
	// levels: string[]; // @deprecated
	// isVisible: boolean; // { type: Boolean, default: false };
}

export interface IDBUserCvReference {
	_id: TypeObjectId<IUserCvReference>;
	name?: string;
	contact?: string;
	order?: number;
	_relation?: TypeObjectId<IReferenceRelation>;
	_position?: TypeObjectId<IReferencePosition>;
	company?: {
		name: string;
		_relatedCompany?: TypeObjectId<ICompany>;
	};
	// _address: {type: Schema.Types.ObjectId, ref: 'Location'},
	address?: IUserGeneralAddress;
	isVisible?: boolean;
}

export interface IDBUserExtra {
	_id: TypeObjectId<IUserExtra>;
	type?: UserExtraType | string;
	title?: string;
	url?: string;
	visible?: boolean;
	originalName?: string;
	date?: Date;
	details?: string;
	uploadDevice?: string;
	antiVirusResult?: IUserExtraAntiVirusResult;
}

export interface IDBCvInfo {
	lastupdate?: Date;
	selectedHighlightExperience?: TypeObjectId<IUserCvExperience>;
	selectedHighlightEducation?: TypeObjectId<IUserCvEducation>;
	experiences?: IDBUserCvExperience[]; // [cvExperienceSchema],
	educations?: IDBUserCvEducation[]; // [cvEducationSchema],
	skills?: IDBUserCvSkill[]; // [cvSkillSchema],
	references?: IDBUserCvReference[]; // [cvReferenceSchema],
	aboutMe?: string;
	hasEducation?: boolean;
	hasExperience?: boolean;
	design?: number;
	font?: CVFont;
	color?: CVColor;
	lineSpacing?: CVLineSpacing;
	disableProfilePic?: boolean;
}

export interface IDBUser {
	_id: TypeObjectId<IUser>;
	createtime: Date;
	lastupdate?: Date;
	locked?: boolean;
	lockedreason?: string;
	lockeddate?: Date;
	_lockedby?: TypeObjectId<IUser>;
	image?: string;
	industry?: string;
	general?: {
		firstName?: string;
		lastName?: string;
		email?: string;
		phone?: string;
		birthday?: Date;
		gender?: Gender;
		interests?: string;
		slogan?: string;
		address?: IUserGeneralAddress;
		_nationality?: TypeObjectId<ICountry>;
	};
	recruiterProfile?: IRecruiterProfile;
	/* tags with skills --> TAGS  (add languages tags here too) */
	// skills: [skillSchema],
	superuser: boolean;
	/* schools, university.. */

	/**
	 * @deprecated use cvInfo.educations - "highlight: true" instead
	 */
	/*
    education: {
        // REFERENZ AKTUELEL AUSBILDUNG
        _recent: any; // { type: Schema.Types.ObjectId }, // ref to one entry of cvInfo.educations

        startDate: Date, // @deprecated
        endDate: Date, // @deprecated
        field: string; // OLD // @deprecated
        _school: TypeObjectId<ISchool>; // { type: Schema.Types.ObjectId, ref: 'School' }, // @deprecated

        _level: TypeObjectId<IEducationLevel>; // { type: Schema.Types.ObjectId, ref: 'Educationlevel' }, // set by highest? or @deprecated
        _sublevel: TypeObjectId<IEducationLevel>; // { type: Schema.Types.ObjectId, ref: 'Educationlevel' }, // set by highest? or @deprecated
    }; */
	/**
	 * @deprecated use cvInfo.experiences - "highlight: true" instead
	 */
	/*
    position: {
        _recent: any; // { type: Schema.Types.ObjectId }, // ref to one entry of cvInfo.experiences

        title: string; // @deprecated
        summary: string; // @deprecated
        startDate: Date, // @deprecated
        endDate: Date, // @deprecated
        isCurrent: boolean; // @deprecated
        _company: TypeObjectId<ICompany>; // { type: Schema.Types.ObjectId, ref: 'Company' }, // @deprecated

        experience: { // @deprecated - this is computed now
            _field: TypeObjectId<IJobField>; // { type: Schema.Types.ObjectId, ref: 'Jobfield' },
            years: number;
        }[],
    }; */
	extras?: IDBUserExtra[];

	local?: {
		id: string; // INDEX
		password: string;
		lastUpdate?: Date;
	};
	localAPI?: {
		id: string; // INDEX
		token: string;
		lastUpdate?: Date;
	};
	facebook?: {
		id: string; // INDEX
		email: string; // INDEX
		name?: string;
		profileLink?: string;
		lastUpdate?: Date;
	};
	linkedin?: {
		id: string; // INDEX
		email: string; // INDEX
		name?: string;
		profileLink?: string;
		lastUpdate?: Date;
	};
	xing?: {
		id: string; // INDEX
		email: string; // INDEX
		name?: string;
		profileLink?: string;
		lastUpdate?: Date;
	};
	google?: {
		id: string; // INDEX
		email: string; // INDEX
		name?: string;
		profileLink?: string;
		lastUpdate?: Date;
	};
	apple?: {
		id: string; // INDEX
		email: string; // INDEX
		name?: string;
		profileLink?: string;
		lastUpdate?: Date;
	};
	jobFilter?: IUserJobFilter;
	// usedCompanys?: TypeObjectId<ICompany>[];
	// credit: number; // { type: number; default: 0 },
	activeJobSearcher?: boolean;
	/* notifications: { // @deprecated
    jobOffer: { // notification if a company likes a user
      push: boolean;
      mail: boolean;
    },
    newJobs: { // notification for new jobs
      push: boolean;
      mail: boolean;
    },
    approveSkills: { // notification for approved skills
      push: boolean;
            // mail: {type: Boolean, default: true}
    },
    newMsg: { // notification for new msgs
            // push: {type: Boolean, default: true},
      mail: boolean;
    },
  }; */
	notificationLevel: number;
	askedForActiveSourcing?: boolean;
	accountVerified?: boolean;
	testerGroup: TesterGroup;
	privacy?: {
		user_register?: Date;
		user_application?: Date;
		user_active_sourcing?: Date;
		company_register?: Date;
		company_posting?: Date;
		company_application?: Date;
		company_club?: Date;
		company_digital_content?: Date;
		user_active_job_searcher?: Date;
	};
	internal?: IUserInternal;
	cvInfo?: IDBCvInfo;
	// _interests: TypeObjectId<IJobField>[]; // [{ type: Schema.Types.ObjectId, ref: 'Jobfield' }],
}

const extrasSchema = new Schema({
	type: String /* portfolio, pdf, website, linkedin, facebook, other */,
	title: String,
	url: String /* url to file or website */,
	order: Number,
	originalName: String,
	date: Date,
	visible: Boolean,
	details: String,
	uploadDevice: String,
	antiVirusResult: {
		timestamp: Date,
		clean: Boolean
	}
});

const competenceSchema = new Schema({
	competence: Number, // 0,1,2,3,4
	_field: { type: Schema.Types.ObjectId, ref: 'Jobfield' } // 2nd level field
});

const cvEducationSchema = new Schema({
	_school: { type: Schema.Types.ObjectId, ref: 'School' },
	_level: { type: Schema.Types.ObjectId, ref: 'Educationlevel' },
	_sublevel: { type: Schema.Types.ObjectId, ref: 'Educationlevel' },
	_degree: { type: Schema.Types.ObjectId, ref: 'Educationdegree' },
	alternative: String, // @deprecated (if school is empty?)
	description: String,
	startDate: Date,
	endDate: Date,
	// isVisible: { type: Boolean, default: false },
	status: { type: String, enum: ['completed', 'canceled', 'studying'] }
});

const cvExperienceSchema = new Schema({
	title: String,
	summary: String,
	company: {
		name: String,
		_relatedCompany: { type: Schema.Types.ObjectId, ref: 'Company' }
	},
	// _company: { type: Schema.Types.ObjectId, ref: 'Company' },
	// _field: { type: Schema.Types.ObjectId, ref: 'Jobfield' }, // @deprecated
	_fields: [{ type: Schema.Types.ObjectId, ref: 'Jobfield' }],
	startDate: Date,
	endDate: Date,
	isCurrent: { type: Boolean, default: false },
	isProfession: { type: Boolean, default: false } // @deprecated
	// isVisible: { type: Boolean, default: false },
});

const cvSkillSchema = new Schema({
	_category: { type: Schema.Types.ObjectId, ref: 'CVSkill' },
	title: String,
	text: String,
	order: Number,
	items: [
		{
			name: String,
			level: Number,
			_id: false
		}
	],
	levels: [String] // @deprecated
	// isVisible: { type: Boolean, default: false },
});

const cvReferenceSchema = new Schema({
	name: String,
	contact: String,
	order: Number,
	_relation: { type: Schema.Types.ObjectId, ref: 'ReferenceRelation' },
	_position: { type: Schema.Types.ObjectId, ref: 'ReferencePosition' },
	company: {
		name: String,
		_relatedCompany: { type: Schema.Types.ObjectId, ref: 'Company' }
	},
	// _company: { type: Schema.Types.ObjectId, ref: 'Company' },
	// _address: {type: Schema.Types.ObjectId, ref: 'Location'},
	address: {
		name: String,
		street: String,
		streetNumber: String,
		district: String,
		city: String,
		county: String,
		country: String,
		code: String,
		longitude: Number,
		latitude: Number,
		countryCode: String
	},
	isVisible: { type: Boolean, default: false }
});

// define the schema for our user model
const userSchema = new Schema({
	createtime: { type: Date, default: Date.now, index: true },
	lastupdate: Date,
	locked: { type: Boolean, default: false },
	lockedreason: String,
	lockeddate: Date,
	_lockedby: { type: Schema.Types.ObjectId, ref: 'User' },
	image: String,
	industry: String,
	general: {
		firstName: String,
		lastName: String,
		email: { type: String, lowercase: true, trim: true },
		phone: String,
		birthday: Date,
		gender: { type: String, enum: [null, 'male', 'female'] },
		interests: String,
		slogan: String,
		// _address: {type: Schema.Types.ObjectId, ref: 'Location'},
		address: {
			name: String,
			street: String,
			streetNumber: String,
			district: String,
			city: String,
			county: String,
			country: String,
			code: String,
			longitude: Number,
			latitude: Number,
			countryCode: String
		},
		_nationality: { type: Schema.Types.ObjectId, ref: 'Country' }
	},
	recruiterProfile: {
		rejectionText: String,
		position: String,
		slogan: String,
		isPrivate: Boolean,
		jobspermonth: String
	},
	/* tags with skills --> TAGS  (add languages tags here too) */
	// skills: [skillSchema],
	superuser: Boolean,
	/* schools, university.. */
	/* education: {
        // REFERENZ AKTUELLE AUSBILDUNG
        _recent: { type: Schema.Types.ObjectId }, // ref to one entry of cvInfo.educations

        startDate: Date, // @deprecated
        endDate: Date, // @deprecated
        _school: { type: Schema.Types.ObjectId, ref: 'School' }, // @deprecated

        _level: { type: Schema.Types.ObjectId, ref: 'Educationlevel' }, // set by highest? or @deprecated
        _sublevel: { type: Schema.Types.ObjectId, ref: 'Educationlevel' }, // set by highest? or @deprecated
    }, */
	/* job experience */
	/*
    position: {
        _recent: { type: Schema.Types.ObjectId }, // ref to one entry of cvInfo.experiences

        title: String, // @deprecated
        summary: String, // @deprecated
        startDate: Date, // @deprecated
        endDate: Date, // @deprecated
        isCurrent: { type: Boolean, default: false },  // @deprecated
        _company: { type: Schema.Types.ObjectId, ref: 'Company' }, // @deprecated

        experience: [{
            _field: { type: Schema.Types.ObjectId, ref: 'Jobfield' },
            years: Number,
        }],
    }, */
	extras: [extrasSchema],
	local: {
		id: {
			type: String,
			index: true,
			lowercase: true,
			trim: true,
			sparse: true
		}, // INDEX
		password: String,
		lastUpdate: Date
	},
	localAPI: {
		id: { type: String, index: true, sparse: true }, // INDEX
		token: String,
		lastUpdate: Date
	},
	facebook: {
		id: { type: String, index: true, sparse: true }, // INDEX
		email: {
			type: String,
			index: true,
			lowercase: true,
			trim: true,
			sparse: true
		}, // INDEX
		name: String,
		profileLink: String,
		lastUpdate: Date
	},
	linkedin: {
		id: { type: String, index: true, sparse: true }, // INDEX
		email: {
			type: String,
			index: true,
			lowercase: true,
			trim: true,
			sparse: true
		}, // INDEX
		name: String,
		profileLink: String,
		lastUpdate: Date
	},
	xing: {
		id: { type: String, index: true, sparse: true }, // INDEX
		email: {
			type: String,
			index: true,
			lowercase: true,
			trim: true,
			sparse: true
		}, // INDEX
		name: String,
		profileLink: String,
		lastUpdate: Date
	},
	google: {
		id: { type: String, index: true, sparse: true }, // INDEX
		email: {
			type: String,
			index: true,
			lowercase: true,
			trim: true,
			sparse: true
		}, // INDEX
		name: String,
		profileLink: String,
		lastUpdate: Date
	},
	apple: {
		id: { type: String, index: true, sparse: true }, // INDEX
		email: {
			type: String,
			index: true,
			lowercase: true,
			trim: true,
			sparse: true
		}, // INDEX
		name: String,
		profileLink: String,
		lastUpdate: Date
	},
	jobFilter: {
		extendSearch: { type: Boolean, default: false },
		lastupdate: { type: Date, default: Date.now },
		_location: { type: Schema.Types.ObjectId, ref: 'Location' }, // location
		_field: [{ type: Schema.Types.ObjectId, ref: 'Jobfield' }],
		region: String, // region for fallback
		searchterm: String,
		filters: [String],
		radius: { type: Number }
	},
	// usedCompanys: [{ type: Schema.Types.ObjectId, ref: 'Company' }],
	credit: { type: Number, default: 0 },
	activeJobSearcher: { type: Boolean, default: false },
	notifications: {
		/* @deprecated */
		jobOffer: {
			// notification if a company likes a user
			push: { type: Boolean, default: true },
			mail: { type: Boolean, default: true }
		},
		newJobs: {
			// notification for new jobs
			push: { type: Boolean, default: true },
			mail: { type: Boolean, default: true }
		},
		approveSkills: {
			// notification for approved skills
			push: { type: Boolean, default: true }
			// mail: {type: Boolean, default: true}
		},
		newMsg: {
			// notification for new msgs
			// push: {type: Boolean, default: true},
			mail: { type: Boolean, default: true }
		}
	},
	notificationLevel: { type: Number, default: 3 },
	askedForActiveSourcing: { type: Boolean, default: false },
	accountVerified: { type: Boolean, default: false },
	testerGroup: String,
	privacy: {
		user_register: Date,
		user_application: Date,
		user_active_sourcing: Date,
		company_register: Date,
		company_posting: Date,
		company_application: Date,
		company_club: Date,
		company_digital_content: Date,
		user_whatsapp: Date,
		user_active_job_searcher: Date
	},
	internal: {
		maxApplicationsWithin7Days: Number,
		maxApplicationsPerCompanyWithin30Days: Number,
		imageUploadDevice: String,
		ga_cid: String,
		skipMessageTypes: {
			// user does not receive messages in here anymore
			push: [String], // mobile
			mail: [String], // mail
			sms: [String] // sms
		},
		companySignup: String,
		userSignup: String,
		utms: [
			{
				source: String,
				medium: String,
				campaign: String,
				content: String,
				date: Date,
				trackedMode: String // signup, login,..
			}
		],
		// tags: [String],
		// _customQuestions: [{ type: Schema.Types.ObjectId, ref: 'Question' }],
		region: String,
		roles: [String],
		lastNewsletterSync: Date,
		verifiedContacts: { type: [String], index: true, sparse: true },
		usedCoupons: [String],
		lastActiveJobNotificationMail: Date,
		lastUserNews: { type: Date, index: true },
		language: { type: String, default: 'de' }, // set by API
		lastLocation: { type: [Number], index: '2d' },
		lastLoginActivity: { type: Date },
		// lastShareYourJobReminder: Date,
		usedLoginDevice: [String],
		registerDevice: String,
		customerId: String,
		brainTreeCustomerId: String,
		lastAccountVerifiedMsg: Date,
		lastAccountVerifiedMsgPhoneDestination: String,
		lastAccountVerifiedMsgMailDestination: String,
		lastTimeActions: {
			anySwipe: Date,
			applied: Date,
			saved: Date,
			jobPublished: Date,
			activeSourced: Date,
			checkoutStarted: Date,
			addCredit: Date,
			sellUp: Date,
			buyCandidate: Date
		},
		firstTimeActions: {
			anySwipe: Date,
			applied: Date,
			saved: Date,
			jobPublished: Date,
			activeSourced: Date,
			checkoutStarted: Date,
			addCredit: Date,
			sellUp: Date,
			buyCandidate: Date
		},
		isManuallyApproved: { type: Boolean, default: false },
		lastReviewDate: Date,
		manualReviewResult: {
			competences: {
				type: [competenceSchema],
				default: undefined
			},
			education: {
				_level: { type: Schema.Types.ObjectId, ref: 'Educationlevel' },
				_sublevel: { type: Schema.Types.ObjectId, ref: 'Educationlevel' },
				_degree: { type: Schema.Types.ObjectId, ref: 'Educationdegree' }
			},
			failedCvCriteria: [String],
			// failedApplicationCriteria: [String],
			notes: String,
			failedCvCriteriaChanged: [String],
			highestEducation: { _level: { type: Schema.Types.ObjectId, ref: 'Educationlevel' } },
			qualitativeAssessment: [String]
		},
		scorings: {
			select: false,
			type: {
				// by user itself
				saved: Number,
				applied: Number,

				// by recruiter
				revealed: Number,
				activeSourced: Number,
				buycontact: Number,

				interesting: Number, // contact request
				rejected: Number // rejection
			}
		},
		candidateAlertMailDates: [Date],
		massApplicationLevel: Number,
		hubspotId: String,
		lastHubspotSync: Date,
		legacyJobList: Boolean,
		pendingDeletion: Date,
		recaptchaResult: {
			score: Number,
			action: String
		},
		seenProductIntros: [String]
	},
	cvInfo: {
		lastupdate: Date,
		selectedHighlightExperience: { type: Schema.Types.ObjectId },
		selectedHighlightEducation: { type: Schema.Types.ObjectId },
		experiences: [cvExperienceSchema],
		educations: [cvEducationSchema],
		skills: [cvSkillSchema],
		references: [cvReferenceSchema],
		aboutMe: String,
		hasEducation: Boolean, // set explicitly to false if user has no education
		hasExperience: Boolean, // set explicitly to false if user has no experience,
		design: Number,
		font: String,
		color: { type: String, enum: AVAILABLE_CV_COLORS },
		lineSpacing: { type: Number, enum: AVAILABLE_CV_LINESPACINGS },
		disableProfilePic: Boolean
	}
	// _interests: [{ type: Schema.Types.ObjectId, ref: 'Jobfield' }]
});

userSchema.set('shardKey', { _id: 1 });

userSchema.index({ 'general.email': 1 }, { sparse: true, background: true });
userSchema.index({ 'general.phone': 1 }, { sparse: true, background: true });
userSchema.index({ 'general.lastName': 1 }, { sparse: true, background: true });

/* index is set via model definition above
userSchema.index({ 'local.id': 1 }, { sparse: true, background: true });
userSchema.index({ 'internal.verifiedContacts': 1 }, { sparse: true, background: true });
userSchema.index({ 'facebook.email': 1 }, { sparse: true });
userSchema.index({ 'google.email': 1 }, { sparse: true });
*/

// create sharded collection:
// use admin
// ##db.runCommand( { shardCollection: "hocknfinder.users", key: { _id: "hashed" }, unique: true } )
// db.runCommand( { shardCollection: "hocknfinder.users", key: { _id: 1 } } )

// for hubspot sync
userSchema.index(
	{ 'internal.lastHubspotSync': 1 },
	{
		partialFilterExpression: {
			'internal.companySignup': { $exists: true }
		},
		background: true
	}
);

/* userSchema.pre('init', function (next) {
 if (this.jobFilter instanceof Array) {
 this.jobFilter = {};
 }
 next();
 }) */
userSchema.index(
	{
		'general.phone': 'text',
		'general.email': 'text',
		'local.id': 'text',
		'facebook.email': 'text',
		'linkedin.email': 'text',
		'google.email': 'text',
		'apple.email': 'text',
		'xing.email': 'text',
		'general.lastName': 'text',
		'internal.verifiedContacts': 'text'
	},
	{ background: true, default_language: 'none', language_override: '_no_language_override' }
);
export const DBUserModel: Model<IDBUser> = model<IDBUser>('User', userSchema);
